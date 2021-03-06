# This file is part of splitsecond.
# https://github.com/globocom/splitsecond

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

# install all dependencies (do not forget to create a virtualenv first)
setup:
	@pip install -U -e .\[tests\]

# test your application (tests in the tests/ directory)
test: unit

unit:
	@coverage run --branch `which nosetests` -vv --with-yanc -s tests/
	@coverage report -m --fail-under=80

# show coverage in html format
coverage-html: unit
	@coverage html

# run tests against all supported python versions
tox:
	@tox

run:
	@splitsecond -c ./splitsecond/splitsecond.conf -ldebug


rebuild: build build-js

build:
	@cd splitsecond/runtime && ./autogen.sh && emconfigure ./configure

build-js:
	@cd splitsecond/runtime && emmake make && emcc -O2 --pre-js prefix.js --post-js postfix.js ./src/splitsecond-splitsecond.o  -o splitsecond.min.js
	@echo
	@echo 'splitsecond.min.js updated at ./splitsecond/runtime/splitsecond.min.js'

build-html:
	@cd splitsecond/runtime && emmake make && emcc -O2 --pre-js prefix.js --post-js postfix.js ./src/splitsecond-splitsecond.o -o splitsecond.html

serve-html:
	@cd splitsecond/runtime && python -mSimpleHTTPServer

kill-explore:
	@-ps aux | egrep -i 'python.+-mSimpleHTTPServer' | egrep -v egrep | awk '{ print $$2 }' | xargs kill -9

explore: kill-explore
	@cd tests/exploratory/ && python -mSimpleHTTPServer &
