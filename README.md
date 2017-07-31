#lyncsmash

a collection of tools to enumerate and attack Microsoft Lync installations

 * find_domain.sh  - an example of how to enumerate the domain for a Lync install
 * lync_smash.py - brute force/user enumeration timing attack in one
 * brute_force_ntlm.sh - an example of a medusa brute force attack against a Lync install


YouTube link: https://www.youtube.com/watch?v=v0NTaCFk6VI

Slide Deck: https://github.com/nyxgeek/lyncsmash/blob/master/DerbyCon%20Files/TheWeakestLync.pdf

If you're looking for username lists, I highly recommend 'Statistically Likely Usernames': https://github.com/insidetrust/statistically-likely-usernames.git


## lync_smash.py
Timing attack to enumerate valid accounts

usage:

enumerating usernames via timing attack
```
python lync_smash.py enum -H 2013-lync-fe.contoso.com -U usernamelist.txt -d CONTOSO
```

discovering domains that are running Lync
```
python lync_smash.py discover -H domain_list.txt
```
locking out a user account
```
python lync_smash.py lock -H 2013-lync-fe.contoso.com -u administrator -d CONTOSO
```
