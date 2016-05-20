#!/bin/bash

DOMAINLIST=$1

if [ -z $DOMAINLIST ]; then
	echo "Usage: ./lyncstink.sh domainlist.txt"
	exit 1
fi



while read -r DOMAIN; do

	if [ -z $DOMAIN ]; then
		continue
	fi

	#this is to check if wildcard is enabled, if it is, then audi 5000
	host -t a x718skal018237hsdfl98123adf098aaa.$DOMAIN  >/dev/null 2>&1
	if [ $? -ne 0 ]; then

		#echo "Testing $DOMAIN"

		#reset i value
		i=0

		#see if the three domains exist, this indicates LYNC presence
		host -t a meet.$DOMAIN >/dev/null 2>&1
		RESULT="$?"
		if [ "$RESULT" -eq "0" ]; then
			i=$((i+1));
		fi

		host -t a lyncdiscover.$DOMAIN >/dev/null 2>&1
		RESULT="$?"
		if [ "$RESULT" -eq "0" ]; then
			i=$((i+1));
		fi

		host -t a dialin.$DOMAIN >/dev/null 2>&1
		RESULT="$?"
		if [ "$RESULT" -eq "0" ]; then
			i=$((i+1));
		fi

		host -t a access.$DOMAIN >/dev/null 2>&1
		RESULT="$?"
		if [ "$RESULT" -eq "0" ]; then
			i=$((i+1));
		fi


		#now choose your own adventure based off of number of results

		case "$i" in
		1)
			Message="FOUND 1 - MAYBE LYNC"
			;;
	        2)
	                Message="FOUND 2 - PROBABLY LYNC"
	                ;;
	        3)
	                Message="FOUND 3 - ALMOST DEFINITELY LYNC"
        	        ;;
	        4)
	                Message="FOUND 4 - THIS IS DEFINITELY LYNC"
        	        ;;

		esac


		#if at least one domain is found then print, otherwise don't say anything
		if [ $i -ne 0 ]; then
			echo "$DOMAIN  - $Message"
		fi
	fi

done < $DOMAINLIST

