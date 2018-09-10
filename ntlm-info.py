#!/usr/bin/env python
#
# ntlm-info.py -- get domain name from NTLM directory on Lync
# 2018 @nyxgeek - TrustedSec
#
# This replicates the functionality of nmap's http-ntlm-info script
# See: https://nmap.org/nsedoc/scripts/http-ntlm-info.html
#
# This can also be done using curl:
# curl -I -s -k --ntlm -u '':'' https://dialin.domain.com  | grep WWW-Authenticate | head -n 1 | cut -d' ' -f3- | base64 -di | xxd -p -  | tr -d '\n' | grep -oe '0200[a-f0-9]\{4,60\}0100' | cut -c9- | rev | cut -c5- | rev  | xxd -r -p
#
# notes: future changes -- cycle through list of known OWA/Skype/Lync NTLM auth directories or define your own
#


import sys
import base64
import re
import requests
from requests_ntlm import HttpNtlmAuth



# check to make sure we have a hostname
arguments = len(sys.argv) - 1

targethost = ''
if ( arguments == 0 ):
   print("You need to specify a Lync/Skype host where the /abs/ directory exists.\n")
   print("Usage:  python ntlm-info.py dialin.testdomain.com\n")
   sys.exit(0)
if ( arguments == 1 ):
   targethost = sys.argv[1]



session = requests.Session()
session.auth = HttpNtlmAuth('','')
r = session.get("https://{0}/abs/".format(targethost))

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
