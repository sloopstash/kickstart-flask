#!/bin/bash

# Install app related packages.
pip install -r /opt/kickstart-flask/requirements.txt

# Modify nginx configuration.
cp /opt/kickstart-flask/config/nginx/main.conf /etc/nginx/nginx.conf
cp /opt/kickstart-flask/config/nginx/app.conf /etc/nginx/conf.d/crm.conf

# Modify supervisor configuration.
cp /opt/kickstart-flask/config/supervisor/main.conf /etc/supervisord.conf

# Add supervisor configuration for app and nginx.
cp /opt/kickstart-flask/config/supervisor/app.ini /etc/supervisord.d/crm.ini
cp /opt/kickstart-flask/config/supervisor/nginx.ini /etc/supervisord.d/nginx.ini
