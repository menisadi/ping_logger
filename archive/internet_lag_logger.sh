#!/bin/bash

# Change the destination log file path
log_file=/var/logs/pings/pings.log

# Replace 'your_router_ip' with the IP address of your router or the server you want to ping
router_ip='8.8.8.8'

# Ping the router and record the result to the log file
ping_result=$(ping -c 1 $router_ip | grep 'bytes from' | cut -d '=' -f 4)
current_time=$(date +"%Y-%m-%d %H:%M:%S")

if [ -n "$ping_result" ]; then
    echo "$current_time - Lag: $ping_result" >> $log_file
else
    echo "$current_time - Request timed out" >> $log_file
fi

