#!/bin/bash

# Check if hostname command exists and get the hostname
if command -v hostname > /dev/null 2>&1; then
    echo "Hostname: $(hostname)"
else
    echo "Hostname command not found."
fi

# Check if /etc/os-release file exists and output its contents
if [ -f /etc/os-release ]; then
    echo "OS Release Info:"
    cat /etc/os-release
else
    echo "/etc/os-release file not found."
fi