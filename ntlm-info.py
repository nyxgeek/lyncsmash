#!/usr/bin/env python
#
# 2018 @nyxgeek - TrustedSec
#
# This replicates the functionality of nmap's http-ntlm-info script
# See: https://nmap.org/nsedoc/scripts/http-ntlm-info.html
#
# This can also be done using curl:
# curl -I -s -k --ntlm -u '':'' https://dialin.domain.com  | grep WWW-Authenticate | head -n 1 | cut -d' ' -f3- | base64 -di | xxd -p -  | tr -d '\n' | grep -oe '0000000f[a-f0-9]\{2,\}0200' | cut -c9- | rev | cut -c5- | rev  | xxd -r -p \n\n")
#
#


import sys
import base64
import re
import requests
from requests_ntlm import HttpNtlmAuth



# check to make sure we have a hostname
arguments = len(sys.argv) - 1

targethost = ''
targetdir = 'abs'

if ( arguments == 0 ):
   print("You need to specify a host, and optionally, a directory to test (default:/abs/)\n")
   print("Usage:  python ntlm-info.py dialin.testdomain.com\n")
   print("Usage:  python ntlm-info.py dialin.testdomain.com WebTicket\n")
   sys.exit(0)
if ( arguments == 1 ):
   targethost = sys.argv[1]

if ( arguments == 2 ):
   targethost = sys.argv[1]
   targetdir = sys.argv[2]


session = requests.Session()
session.auth = HttpNtlmAuth('','')
try:
    r = session.get("https://{0}/{1}/".format(targethost,targetdir))
    ntlmkey = (r.request.headers['Authorization']).split(" ")[1]
    ntlmhex = (base64.b64decode(ntlmkey)).encode("hex")

    print("Hex is: {0}".format(ntlmhex))

    # regex to search for our 0200 at beginning and 0100 at end
    searchObj = re.search( r'0200([0-9a-fA-F]{4,60})0100', ntlmhex, re.M|re.I)

    if searchObj:
       # get only the subsection we want, inside of our markers
       regexresult = searchObj.group()[8:-4]

       # break into 2-char chunks
       n=2
       regexarray = [regexresult[i:i+n] for i in range(0, len(regexresult), n)]
       # remove the 00 entries
       while '00' in regexarray: regexarray.remove('00')
       print("{}".format(regexarray))

       # join the array together
       hexstring = ''.join(regexarray)
       # convert to ascii
       print("NetBIOS Name: {0}".format(hexstring.decode("hex")))


    else:
       print("Could not find our markers 0200 and 0100\n")
       exit
except:
   print("Unable to connect - make sure it is an NTLM auth dir")
