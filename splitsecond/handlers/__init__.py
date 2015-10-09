#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of splitsecond.
# https://github.com/globocom/splitsecond

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

import traceback

import tornado.web

from splitsecond.context import Context
from splitsecond.utils import logger


HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"


class BaseHandler(tornado.web.RequestHandler):
    def _error(self, status, msg=None):
        self.set_status(status)
        if msg is not None:
            logger.warn(msg)
        self.finish()


class ContextHandler(BaseHandler):
    def initialize(self, context):
        self.context = Context(
            server=context.server,
            config=context.config,
            importer=context.modules.importer,
            request_handler=self
        )

    def log_exception(self, *exc_info):
        if isinstance(exc_info[1], tornado.web.HTTPError):
            # Delegate HTTPError's to the base class
            # We don't want these through normal exception handling
            return super(ContextHandler, self).log_exception(*exc_info)

        msg = traceback.format_exception(*exc_info)

        try:
            if self.context.config.USE_CUSTOM_ERROR_HANDLING:
                self.context.modules.importer.error_handler.handle_error(context=self.context, handler=self, exception=exc_info)
        finally:
            del exc_info
            logger.error('ERROR: %s' % "".join(msg))
