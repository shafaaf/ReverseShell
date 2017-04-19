#!/bin/bash

# This kills procecss and removes the executables etc and leaves only source code

kill -9 $(lsof -i:9999 -t) 2> /dev/null

rm -rf trick/
rm -rf trick.*
