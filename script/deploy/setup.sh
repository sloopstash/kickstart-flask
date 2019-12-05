#!/bin/bash

# Install system packages.
yum -y update
yum install -y ruby git python-devel python-setuptools wget vim net-tools initscripts gcc make tar bind-utils nc
easy_install supervisor pip

# Make supervisor configuration directory.
mkdir -p /etc/supervisord.d

# Make app directory.
mkdir -p /opt/kickstart-flask
