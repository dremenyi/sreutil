#!/bin/bash

# Function to check if FIPS is enabled
check_fips() {
    if [ -f /proc/sys/crypto/fips_enabled ]; then
        fips_status=$(cat /proc/sys/crypto/fips_enabled)
        if [ "$fips_status" -eq 1 ]; then
            hostname=$(hostname)
            echo ""
            echo "status returned $fips_status for $hostname"
            echo ""
            echo "FIPS is enabled"
        else
            echo "status returned $fips_status for $hostname"
            echo ""
            echo "FIPS is not enabled"
        fi
    else
        echo "FIPS is not enabled"
    fi
}

# Get the hostname of the EC2 instance


# Check if FIPS is enabled
check_fips