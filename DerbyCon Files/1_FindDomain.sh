#!/bin/bash

echo "Finding domain for 2013-lync-fe.contoso.com"
echo "Command: nmap -sS -p443 --script http-ntlm-info 2013-lync-fe.contoso.com"

nmap -sS -p443 --script http-ntlm-info 2013-lync-fe.contoso.com
