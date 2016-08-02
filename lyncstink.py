#!/usr/bin/python

import urllib2
import sys, getopt, os, ssl

###############################################################################
# # # # # # # # # # # # # # # # # #    VARS    # # # # # # # # # # # # # # # #
###############################################################################


subdomains = ["dialin", "meet", "lyncdiscover", "dialin", "access", "lync"]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


###############################################################################
# # # # # # # # # # # # # # # # # #    DEFS    # # # # # # # # # # # # # # # #
###############################################################################


def checkstatus(testurl):

   #set variable to count the number of indicators
   indicatorcount = 0

   #first let's check for the common subdomains, so
   #loop through our array of subdomains
   startingpoint = 0
   while startingpoint < len(subdomains):
        subdomain = subdomains[startingpoint]
        tmpdomain = subdomain + "." + testurl
        print "+ Trying %s" % tmpdomain


        try: 
            responsecode = urllib2.urlopen("https://" + tmpdomain, context=ctx, timeout=3).getcode()
            indicatorcount += 1
        except:
            sys.stdout.write('')
        startingpoint += 1

   return indicatorcount

###############################################################################
# # # # # # # # # # # # # # # # # #    MAIN    # # # # # # # # # # # # # # # #
###############################################################################

# Store input and output file names
ifile=''
ofile=''
 
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:o:")
 
for o, a in myopts:
    if o == '-i':
        ifile=a
    elif o == '-o':
        ofile=a
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])
 
inputfilepath = ((os.path.dirname(os.path.abspath(__file__))) + "/%s") % ifile

with open(inputfilepath) as parsedfile:
    data = {}
    lines = (line.rstrip() for line in parsedfile)
    lines = (line for line in lines if line)

    for line in lines:
        print "--------------------------------------------"
	print "Testing %s" % line
        results = checkstatus(line)
        print "Found %d indicators for %s" % (results, line)
        if results != 0:
            data[line] = results


    print data
