#!/bin/bash
HOST=$1

if [ -z $HOST ]; then
	echo "Usage: ./find_domain.sh <lync_host>"
	exit 1
fi

echo "Finding domain for $HOST"
echo ""
echo "Command:"
echo "nmap -sS -p443 --script http-ntlm-info $HOST"

nmap -sS -p443 --script http-ntlm-info $HOST
