#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of splitsecond.
# https://github.com/globocom/splitsecond

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

import tornado.web
import tornado.ioloop

from splitsecond.handlers.healthcheck import HealthcheckHandler


class SplitSecondServiceApp(tornado.web.Application):

    def __init__(self, context):
        self.context = context
        super(SplitSecondServiceApp, self).__init__(self.get_handlers())

    def get_handlers(self):
        handlers = [
            (r'/healthcheck', HealthcheckHandler),
        ]

        return handlers
