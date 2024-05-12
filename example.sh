#!/usr/bin/env bash

# Build a docker image
docker build -t app-the-gathering .

# Make an AppImage from /examples/apps.json
docker run -v ./examples:/src app-the-gathering

# make a softlink likely BusyBox for execution
ln -s ./examples/gather.AppImage ./date

# execute a date command!
./date
