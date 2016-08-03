# lyncstink
Locate domains that are running Lync servers


When Lync is published externally it is often set up with a number of subdomains. These include:

 * lyncdiscover.domain.com
 * access.domain.com
 * meet.domain.com
 * dialin.domain.com


This script will check a domain to see if these exist. It also checks for a long random 
subdomain in order to exclude wildcarded domains.


## Example output

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
