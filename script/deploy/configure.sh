#!/bin/bash

# Install required packages for app.
pip install -r /opt/app/requirements.txt

# Modify supervisor configuration.
cp /opt/app/config/supervisor/main.conf /etc/supervisord.conf

# Add supervisor configuration for app.
cp /opt/app/config/supervisor/app.ini /etc/supervisord.d/app.ini
