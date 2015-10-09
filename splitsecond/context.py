#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of splitsecond.
# https://github.com/globocom/splitsecond

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

import tornado
from concurrent.futures import ThreadPoolExecutor, Future
import functools


class Context:
    '''
    Class responsible for containing:
    * Server Configuration Parameters (port, ip, key, etc);
    * Configurations read from config file (or defaults);
    * Importer with imported modules (loader, storage, optimizers);
    * Request Parameters (page url).

    Each instance of this class MUST be unique per request. This class should not be cached in the server.
    '''

    def __init__(self, server=None, config=None, importer=None, request_handler=None):
        self.server = server
        self.config = config
        if importer:
            self.modules = ContextImporter(self, importer)
        else:
            self.modules = None

        self.request_handler = request_handler
        self.thread_pool = ThreadPool.instance(getattr(config, 'ENGINE_THREADPOOL_SIZE', 0))
        self.headers = {}


class ServerParameters(object):
    def __init__(self, port, ip, config_path, log_level, fd=None):
        self.port = port
        self.ip = ip
        self.config_path = config_path
        self.log_level = log_level
        self.fd = fd


class RequestParameters:
    def __init__(self, page_url):
        self.page_url = page_url


class ContextImporter:
    def __init__(self, context, importer):
        self.context = context
        self.importer = importer

        self.loader = None
        if importer.loader:
            self.loader = importer.loader

        self.optimizers = importer.optimizers


class ThreadPool(object):

    @classmethod
    def instance(cls, size):
        """
        Cache threadpool since context is
        recreated for each request
        """
        if not hasattr(cls, "_instance"):
            cls._instance = ThreadPool(size)
        return cls._instance

    def __init__(self, thread_pool_size):
        if thread_pool_size:
            self.pool = ThreadPoolExecutor(thread_pool_size)
        else:
            self.pool = None

    def _execute_in_foreground(self, operation, callback):
        result = Future()
        result.set_result(operation())
        callback(result)

    def _execute_in_pool(self, operation, callback):
        task = self.pool.submit(operation)
        task.add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                functools.partial(callback, future)
            )
        )

    def queue(self, operation, callback):
        if not self.pool:
            self._execute_in_foreground(operation, callback)
        else:
            self._execute_in_pool(operation, callback)

    def cleanup(self):
        if self.pool:
            print "Joining threads...."
            self.pool.shutdown()
