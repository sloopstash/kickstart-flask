#!/bin/bash

# Update modified configuration if any.
/usr/bin/supervisorctl update all

# Restart all supervisor manged programs.
/usr/bin/supervisorctl restart all