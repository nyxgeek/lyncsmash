```
██╗  ██╗   ██╗███╗   ██╗ ██████╗███████╗███╗   ███╗ █████╗ ███████╗██╗  ██╗
██║  ╚██╗ ██╔╝████╗  ██║██╔════╝██╔════╝████╗ ████║██╔══██╗██╔════╝██║  ██║
██║   ╚████╔╝ ██╔██╗ ██║██║     ███████╗██╔████╔██║███████║███████╗███████║
██║    ╚██╔╝  ██║╚██╗██║██║     ╚════██║██║╚██╔╝██║██╔══██║╚════██║██╔══██║
███████╗██║   ██║ ╚████║╚██████╗███████║██║ ╚═╝ ██║██║  ██║███████║██║  ██║
╚══════╝╚═╝   ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
```                                                                   


a collection of tools to enumerate and attack self-hosted Skype for Business and Microsoft Lync installations

*Note: these tools will not work with Skype/Lync installations hosted at Microsoft.*
<hr>

DerbyCon 6.0 YouTube link: https://www.youtube.com/watch?v=v0NTaCFk6VI

DerbyCon 6.0 Slide Deck: https://github.com/nyxgeek/nyxgeek-slides/blob/master/TheWeakestLync.pdf


## scripts
 * lyncsmash.py - enumerate users via auth timing bug while brute forcing, lock accounts, locate lync installs
 * find_domain.sh  - example of how to use Nmap with http-ntlm-info script to discover internal NetBIOS & domain names
 * brute_force_ntlm.sh - example of a brute force attack against Skype/Lync using Medusa
 * ntlm-info.py - script to get NetBIOS Domain name from NTLM auth

## wordlists
 * skype-directories.txt - a listing of directories that may have NTLM-auth enabled
 * alexa-top-20000-sites.txt - a listing of the top 20,000 Alexa sites - to be used with discover mode

If you're looking for username lists, I highly recommend 'Statistically Likely Usernames': https://github.com/insidetrust/statistically-likely-usernames.git

<hr>

## using lyncsmash.py

lyncsmash has three operating modes:
 * enum - use to enumerate users via the auth timing attack
 * discover - will take a list of domains and determine which use Skype for Business/Lync
 * lock - make repeated bad authentication attempts in order to lock out an account



### lyncsmash.py enum - enumerate users

** WARNING: THIS PERFORMS A DOMAIN LOGIN ATTEMPT AND CAN LOCK OUT ACCOUNTS **

```
Parameters:
    -H	hostname
    -U	username list
    -p  password
    -P  password list
    -d	domain
    -o  output file
```
In this mode lyncsmash will enumerate usernames via a timing attack, using the Webticket service located on the Lync Front-End server. If a bad username and/or domain is specified, the response will be long. If it is a valid user, the response will be short. Due to limitations of the timing-attack, this can only be run single-threaded.


usage:
```
python lyncsmash.py enum -H 2013-lync-fe.contoso.com -U usernamelist.txt -P passwordlist.txt -d CONTOSO -o CONTOSO_output.txt

or

python lyncsmash.py enum -H 2013-lync-fe.contoso.com -U usernamelist.txt -p Winter2017 -d CONTOSO

```

### lyncsmash.py discover - discovering domains that are running Skype/Lync

```
Parameters:
    -H	host list - one domain per line
```
In this mode lyncsmash will attempt to enumerate various Skype/Lync subdomains via DNS, and returns a score based on number of indicators. Wildcard domains are discarded.

usage:
```
python lyncsmash.py discover -H domain_list.txt

```

### lyncsmash lock - lockout an account with repeated login failures
** WARNING: THIS WILL LOCK OUT ACCOUNTS. **

```
Parameters:
    -H	hostname
    -u	username to lock out
    -d	domain
```

In this mode lyncsmash will make 5 login attempts with an incorrect password, attempting to lock out a user account.


usage:
```
python lyncsmash.py lock -H 2013-lync-fe.contoso.com -u administrator -d CONTOSO

```

<hr>

## ntlm-info.py

This script examines the HTTP headers from a null NTLM auth attempt.  It will test against the /abs/ directory by default but any directory can be specified as a second argument (see below). This is a remake of the http-ntlm-info script from nmap (https://nmap.org/nsedoc/scripts/http-ntlm-info.html).

Additional potential NTLM auth directories can be found in this repository under wordlists (https://github.com/nyxgeek/lyncsmash/blob/master/wordlists/skype-directories.txt).

Requires requests_ntlm -- install with:

```pip install requests_ntlm```

Usage:
```
python ntlm-info.py dialin.domain.com

python ntlm-info.py dialin.domain.com RequestHandlerExt
```

## thanks!
Thanks to @coldfusion39, @spoonman1091, and @shellfail for contributing fixes and improvements!
