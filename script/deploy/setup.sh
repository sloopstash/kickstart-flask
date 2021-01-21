#!/bin/bash

# Make app directory.
APP_DIR=/opt/app
if [ -d "$APP_DIR" ]; then
  rm -r $APP_DIR
fi
mkdir -p $APP_DIR
