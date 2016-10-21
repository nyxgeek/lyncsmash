#lyncsmash

a collection of tools to enumerate and attack Microsoft Lync installations

 * find_domain.sh  - an example of how to enumerate the domain for a Lync install
 * lync_smash.py - brute force/user enumeration timing attack in one
 * brute_force_ntlm.sh - an example of a medusa brute force attack against a Lync install


YouTube link: https://www.youtube.com/watch?v=v0NTaCFk6VI

Slide Deck: https://github.com/nyxgeek/lyncsmash/blob/master/DerbyCon%20Files/TheWeakestLync.pdf

## lyncstink
Locate domains that are running Lync servers


When Lync is published externally it is often set up with a number of subdomains. These include:

 * lyncdiscover.domain.com
 * access.domain.com
 * meet.domain.com
 * dialin.domain.com


This script will check a domain to see if these exist. It also checks for a long random 
subdomain in order to exclude wildcarded domains.


### Example output

```
yahoo.com  - FOUND 1 - MAYBE LYNC
baidu.com  - FOUND 4 - THIS IS DEFINITELY LYNC
twitter.com  - FOUND 1 - MAYBE LYNC
qq.com  - FOUND 1 - MAYBE LYNC
ebay.com  - FOUND 1 - MAYBE LYNC
ask.com  - FOUND 1 - MAYBE LYNC
paypal.com  - FOUND 1 - MAYBE LYNC
microsoft.com  - FOUND 3 - ALMOST DEFINITELY LYNC
adobe.com  - FOUND 2 - PROBABLY LYNC
bbc.co.uk  - FOUND 3 - ALMOST DEFINITELY LYNC
cnn.com  - FOUND 2 - PROBABLY LYNC
netflix.com  - FOUND 1 - MAYBE LYNC
```
