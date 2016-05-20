# lyncstink
Locate domains that are running Lync servers


When Lync is published externally it requires a number of subdomains. These include:


 * access.domain.com
 * meet.domain.com
 * dialin.domain.com


This script will check a domain to see if these exist. It also checks for a long random 
subdomain in order to exclude wildcarded domains.
