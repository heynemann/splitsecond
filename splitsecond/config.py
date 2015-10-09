#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of splitsecond.
# https://github.com/globocom/splitsecond

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

import derpconf.config as config
from derpconf.config import Config

from splitsecond.version import __version__


Config.define('SPLITSECOND_LOG_CONFIG', None, 'Logging configuration as json', 'Logging')

Config.define(
    'SPLITSECOND_LOG_FORMAT', '%(asctime)s %(name)s:%(levelname)s %(message)s',
    'Log Format to be used by split second when writing log messages.', 'Logging')

Config.define(
    'SPLITSECOND_LOG_DATE_FORMAT', '%Y-%m-%d %H:%M:%S',
    'Date Format to be used by splitsecond when writing log messages.', 'Logging')

Config.define(
    'LOADER', 'splitsecond.loaders.http_loader', 'Class to load assets with.', 'Loader'
)

Config.define(
    'OPTIMIZERS', [], 'Optimizers to run on assets.', 'Optimizers'
)


# HTTP LOADER OPTIONS
Config.define(
    'HTTP_LOADER_CONNECT_TIMEOUT', 5,
    'The maximum number of seconds libcurl can take to connect to an asset being loaded', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_REQUEST_TIMEOUT', 20,
    'The maximum number of seconds libcurl can take to download an asset', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_FOLLOW_REDIRECTS', True,
    'Indicates whether libcurl should follow redirects when downloading an asset', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_MAX_REDIRECTS', 5,
    'Indicates the number of redirects libcurl should follow when downloading an asset', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_MAX_CLIENTS', 10,
    'The maximum number of simultaneous HTTP connections the loader can make before queuing', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_FORWARD_USER_AGENT', False,
    'Indicates whether splitsecond should forward the user agent of the requesting user', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_DEFAULT_USER_AGENT', "SplitSecond/%s" % __version__,
    'Default user agent for splitsecond http loader requests', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_PROXY_HOST', None,
    'The proxy host needed to load assets through', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_PROXY_PORT', None,
    'The proxy port for the proxy host', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_PROXY_USERNAME', None,
    'The proxy username for the proxy host', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_PROXY_PASSWORD', None,
    'The proxy password for the proxy host', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_CA_CERTS', None,
    'The filename of CA certificates in PEM format', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_CLIENT_KEY', None,
    'The filename for client SSL key', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_CLIENT_CERT', None,
    'The filename for client SSL certificate', 'HTTP Loader')
Config.define(
    'HTTP_LOADER_CURL_ASYNC_HTTP_CLIENT', False,
    'If the CurlAsyncHTTPClient should be used', 'HTTP Loader')


def generate_config():
    config.generate_config()


if __name__ == '__main__':
    generate_config()
