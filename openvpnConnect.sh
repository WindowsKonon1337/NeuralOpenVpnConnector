#!/bin/bash

cd ~/scripts/utils/src
ConfigFile='vpnConfig.tmp'
echo 'write username (freeopenvpn by default): ' 

read username

if [$username == '']
then
    echo 'freeopenvpn' > $ConfigFile 
else
     echo $username > $ConfigFile
fi
echo 'write password (will be parsed by default): '

read password

if [$password == '']
then
    python3 ./openvpnConnect/getPassword.py >> $ConfigFile
else
     echo $password >> $ConfigFile
fi

sudo openvpn --config ~/Desktop/Netherlands_freeopenvpn_tcp.ovpn  --auth-user-pass "$ConfigFile" 

rm $ConfigFile