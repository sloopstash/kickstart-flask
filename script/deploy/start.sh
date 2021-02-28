#!/bin/bash

# Update modified configuration if any.
/usr/bin/supervisorctl update all

# Restart all Supervisor manged programs.
/usr/bin/supervisorctl restart all