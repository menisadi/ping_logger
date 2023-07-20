#!/bin/bash
date +%D-%H:%M:%S >> /Users/meni/Code/personal/InternetLagLogger/pinger.log
/sbin/ping -c 1 '8.8.8.8' >> /Users/meni/Code/personal/InternetLagLogger/pinger.log
