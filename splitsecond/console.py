#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of splitsecond.
# https://github.com/globocom/splitsecond

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>


import optparse

from splitsecond.context import ServerParameters
from splitsecond import __version__


def get_server_parameters(arguments=None):
    parser = optparse.OptionParser(
        usage="splitsecond or type splitsecond -h (--help) for help", description=__doc__, version=__version__
    )
    parser.add_option(
        "-p", "--port", type="int", dest="port", default=9999,
        help="The port to run this splitsecond instance at [default: %default]."
    )
    parser.add_option(
        "-i", "--ip", dest="ip", default="0.0.0.0",
        help="The host address to run this splitsecond instance at [default: %default]."
    )
    parser.add_option(
        "-f", "--fd", dest="file_descriptor",
        help="The file descriptor number or path to listen for connections on (--port and --ip will be ignored if this is set)"
        "[default: %default]."
    )
    parser.add_option(
        "-c", "--conf", dest="conf", default="",
        help="The path of the configuration file to use for this splitsecond instance [default: %default]."
    )
    parser.add_option(
        "-l", "--log-level", dest="log_level", default="warning",
        help="The log level to be used. Possible values are: debug, info, warning, error, critical or notset. "
        "[default: %default]."
    )

    (options, args) = parser.parse_args(arguments)

    port = options.port
    ip = options.ip
    fd = options.file_descriptor
    conf = options.conf or None
    log_level = options.log_level

    return ServerParameters(
        port=port,
        ip=ip,
        config_path=conf,
        log_level=log_level,
        fd=fd
    )
