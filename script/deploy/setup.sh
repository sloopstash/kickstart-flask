#!/bin/bash

# Install system packages.
yum -y update
yum install -y ruby git python-devel python-setuptools wget vim net-tools initscripts gcc make tar bind-utils nc

# Install nginx.
wget https://nginx.org/packages/rhel/7/x86_64/RPMS/nginx-1.14.0-1.el7_4.ngx.x86_64.rpm
yum install -y nginx-1.14.0-1.el7_4.ngx.x86_64.rpm
rm nginx-1.14.0-1.el7_4.ngx.x86_64.rpm

# Install supervisor.
easy_install supervisor pip

# Make supervisor configuration directory.
mkdir -p /etc/supervisord.d

# Make app directory.
APP_DIR=/opt/app
if [ -d "$APP_DIR" ]; then
  rm -r $APP_DIR
fi
mkdir -p $APP_DIR
