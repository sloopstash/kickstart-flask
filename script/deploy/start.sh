#!/bin/bash

# Run supervisor in the background.
/usr/bin/supervisord -c /etc/supervisord.conf

# Restart all supervisor manged programs.
/usr/bin/supervisorctl restart all