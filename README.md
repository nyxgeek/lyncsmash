# lyncsmash

a collection of tools to enumerate and attack self-hosted Skype for Business and Microsoft Lync installations that are externally accessible.
*Note: these tools will not work with Skype/Lync installations hosted at Microsoft.*


DerbyCon 6.0 YouTube link: https://www.youtube.com/watch?v=v0NTaCFk6VI

DerbyCon 6.0 Slide Deck: https://github.com/nyxgeek/lyncsmash/blob/master/DerbyCon%20Files/TheWeakestLync.pdf


## scripts
 * lyncsmash.py - enumerate users via auth timing bug while brute forcing, lock accounts, locate lync installs
 * find_domain.sh  - example of how to use Nmap with http-ntlm-info script to discover internal NetBIOS & domain names
 * brute_force_ntlm.sh - example of a brute force attack against Skype/Lync using Medusa

## wordlists
 * skype-directories.txt - a listing of directories that may have NTLM-auth enabled
 * alexa-top-20000-sites.txt - a listing of the top 20,000 Alexa sites - to be used with discover mode

If you're looking for username lists, I highly recommend 'Statistically Likely Usernames': https://github.com/insidetrust/statistically-likely-usernames.git


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
    -p  password to use
    -d	domain
```
In this mode lyncsmash will enumerate usernames via a timing attack, using the Webticket service located on the Lync Front-End server. If a bad username and/or domain is specified, the response will be long. If it is a valid user, the response will be short. Due to limitations of the timing-attack, this can only be run single-thraded.


usage:
```
python lync_smash.py enum -H 2013-lync-fe.contoso.com -U usernamelist.txt -p Summer2017 -d CONTOSO

```

### lyncsmash.py discover - discovering domains that are running Skype/Lync

```
Parameters:
    -H	host list - one domain per line
```
In this mode lyncsmash will attempt to enumerate various Skype/Lync subdomains via DNS, and returns a score based on number of indicators. Wildcard domains are discarded.

usage:
```
python lync_smash.py discover -H domain_list.txt

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
python lync_smash.py lock -H 2013-lync-fe.contoso.com -u administrator -d CONTOSO

```


## thanks!
Thanks to @coldfusion39 and @spoonman1091 for contributing fixes and improvements!
