#!/bin/bash

# Install required packages for app.
pip install -r /opt/app/requirements.txt

# Modify supervisor configuration.
cp /opt/app/config/supervisor/main.conf /etc/supervisord.conf

# Add supervisor configuration for app.
cp /opt/app/config/supervisor/app.ini /etc/supervisord.d/app.ini

DEFAULT_REDIS_HOST="crm-redis"
REDIS_HOST=$(aws ssm get-parameter --name CRM-PRD-Redis-Host --query Parameter.Value --region us-west-2)
sed -i 's|"'$DEFAULT_REDIS_HOST'"|'$REDIS_HOST'|g' /opt/app/config/redis.conf

DEFAULT_STATIC_ENDPOINT="http://app.crm"
STATIC_ENDPOINT=$(aws ssm get-parameter --name CRM-PRD-STT-END --query Parameter.Value --region us-west-2)
sed -i 's|"'$DEFAULT_STATIC_ENDPOINT'"|'$STATIC_ENDPOINT'|g' /opt/app/config/app.conf
sed -i 's|"dev"|"prd"|g' /opt/app/config/app.conf