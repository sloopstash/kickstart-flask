#!/bin/bash

# Install system packages.
yum -y update
yum install -y ruby git python-devel python-setuptools wget vim net-tools initscripts gcc make tar bind-utils nc

# Make app directory.
APP_DIR=/opt/app
if [ -d "$APP_DIR" ]; then
  rm -r $APP_DIR
fi
mkdir -p $APP_DIR
