#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of splitsecond.
# https://github.com/globocom/splitsecond

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

import sys
import logging
import logging.config

import os
import socket
from os.path import expanduser, dirname

import tornado.ioloop
from tornado.httpserver import HTTPServer

from splitsecond.console import get_server_parameters
from splitsecond.config import Config
from splitsecond.importer import Importer
from splitsecond.context import Context
from splitsecond.app import SplitSecondServiceApp


def get_as_integer(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def get_config(config_path):
    lookup_paths = [os.curdir,
                    expanduser('~'),
                    '/etc/',
                    dirname(__file__)]

    return Config.load(config_path, conf_name='splitsecond.conf', lookup_paths=lookup_paths)


def configure_log(config, log_level):
    if (config.SPLITSECOND_LOG_CONFIG and config.SPLITSECOND_LOG_CONFIG != ''):
        logging.config.dictConfig(config.SPLITSECOND_LOG_CONFIG)
    else:
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=config.SPLITSECOND_LOG_FORMAT,
            datefmt=config.SPLITSECOND_LOG_DATE_FORMAT
        )


def get_importer(config):
    importer = Importer(config)
    importer.import_modules()

    return importer


def get_context(server_parameters, config, importer):
    return Context(
        server=server_parameters,
        config=config,
        importer=importer
    )


def get_application(context):
    return SplitSecondServiceApp(context)


def run_server(application, context):
    server = HTTPServer(application)

    if context.server.fd is not None:
        fd_number = get_as_integer(context.server.fd)
        if fd_number is None:
            with open(context.server.fd, 'r') as sock:
                fd_number = sock.fileno()

        sock = socket.fromfd(fd_number,
                             socket.AF_INET | socket.AF_INET6,
                             socket.SOCK_STREAM)
        server.add_socket(sock)
    else:
        server.bind(context.server.port, context.server.ip)

    server.start(1)


def main(arguments=None):
    '''Runs splitsecond server with the specified arguments.'''

    server_parameters = get_server_parameters(arguments)
    config = get_config(server_parameters.config_path)
    configure_log(config, server_parameters.log_level.upper())

    importer = get_importer(config)

    context = get_context(server_parameters, config, importer)

    application = get_application(context)
    run_server(application, context)

    try:
        logging.debug('splitsecond running at %s:%d' % (context.server.ip, context.server.port))
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        sys.stdout.write('\n')
        sys.stdout.write("-- splitsecond closed by user interruption --\n")
    finally:
        context.thread_pool.cleanup()

if __name__ == "__main__":
    main(sys.argv[1:])
