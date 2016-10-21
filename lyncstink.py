#!/usr/bin/python

import urllib2
import sys, getopt, os, ssl, csv

###############################################################################
# # # # # # # # # # # # # # # # # #    VARS    # # # # # # # # # # # # # # # #
###############################################################################


subdomains = ["dialin", "meet", "lyncdiscover", "dialin", "access", "lync", "lyncext", "lyncaccess01", "lyncaccess"]

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
 
        #first try to see if they have wildcard turned on, if so, gtfo
        try:
             testwildcard = urllib2.urlopen("https://a8120jksdpadsf1834jk1212319023471nasdfnv8zalsdfoqpxcv." + testurl, context=ctx, timeout=3).getcode()
             if (testwildcard == 200):
                print "FOUND WILDCARD DOMAIN - time to GTFO"
                startingpoint += 1
                break
        except:
              sys.stdout.write('')

        try: 
            responsecode = urllib2.urlopen("https://" + tmpdomain, context=ctx, timeout=3).getcode()
            indicatorcount += 1
        except:
            sys.stdout.write('')
        startingpoint += 1

   return indicatorcount


def writecsv(filename,dict):
    with open(filename, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dict.items():
           writer.writerow([key, value])

###############################################################################
# # # # # # # # # # # # # # # # # #    MAIN    # # # # # # # # # # # # # # # #
###############################################################################

# Store input and output file names
ifile=''
ofile=''
 
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:o:")

if len(myopts) == 0:
    print "usage: ./lyncstink.py -i <inputfile> -o <outputfile>"
    sys.exit()
 
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
    writecsv(ofile,data)
