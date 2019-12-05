#!/bin/bash

# Install app related packages.
pip install -r /opt/kickstart-flask/requirements.txt

# Modify supervisor configuration.
cp /opt/kickstart-flask/config/supervisor/main.conf /etc/supervisord.conf

# Add supervisor configuration for app and nginx.
cp /opt/kickstart-flask/config/supervisor/app.ini /etc/supervisord.d/crm.ini
