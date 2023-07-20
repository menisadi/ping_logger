(date +%D-%H:%M:%S ; ping -qn -c2 8.8.8.8 2>&1 | grep "packets transmitted") >> ~/code/personal/InternetLagLogger/lags.log
