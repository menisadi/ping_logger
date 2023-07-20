#!/bin/bash


ping -qn -W4 -c2 8.8.8.8 2>&1 | xargs -iX date +"%Y-%m-%d %H:%M:%S X" >> "~/code/personal/internetlaglogger/pings.log" 2>&1

