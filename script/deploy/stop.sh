#!/bin/bash

# Stop all supervisor managed programs.
/usr/bin/supervisorctl stop all

# Shutdown supervisor.
/usr/bin/supervisorctl shutdown