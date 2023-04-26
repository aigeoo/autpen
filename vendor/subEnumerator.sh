#!/bin/bash

if [ -z $1 ]
	then
		echo "USAGE: ./$0 [domain] (optional: subdomains file to skip first stage)"
		exit
	else
		target=$1
	
fi

if [ -z $2 ]
then
	# Get subdomains from subfinder
	subfinder -d $target -silent > subdomains1.txt
	echo "[+] subfinder tool result saved in subdomains1.txt" 

	# Get subdomains from assetfinder
	assetfinder $target -subs-only > subdomains2.txt
	echo "[+] assetfinder tool result saved in subdomains2.txt"

	# Get subdomains from sublist3r
	sublist3r -n -d $target -o subdomains3.txt
	echo "[+] sublist3r tool result saved in subdomains3.txt" 

	# Get subdomains from knockpy
	knockpy --no-http $target
	cat knockpy_report/$target* | grep -oP '[a-z0-9]+\.'$target | sort -u | uniq > subdomains4.txt
	echo "[+] knockpy tool result saved in subdomains5.txt"

	# bruteforce subdomains 
	awk -v host=$target '{print $0"."host}' /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt > massdnslist
	massdns massdnslist -r /usr/share/seclists/Miscellaneous/dns-resolvers.txt -o S -t A -q | awk -F". " '{print $1}' | sort -u  > subdomains5.txt
	echo "[+] massdns tool result saved in subdomains6.txt" 

	# sort and organize the outputs
	echo "[+] Sorting the result in one file 'finaldomains.txt'"
	cat subdomains*.txt | grep -i $target | sort -u | uniq > allSubdomain_$target.txt
	echo "[+] Domains found: "$(cat allSubdomain_$target.txt | wc -l)
	echo "[+] Tool finished getting all subdomains"
	alldomains=allSubdomain_$target.txt
	rm -rf subdomains*.txt
else
	alldomains=$2
fi
	echo "[+] Getting alive domains ..."
	httpx -l $alldomains -silent -timeout 20 -title -tech-detect -status-code -follow-redirects -probe -o subdomains_$target_alive_titel.txt
	echo "[+] Details of alive domains saved in 'subdomains_$target_alive_titel.txt' file"
	cat alive_titles.txt | cut -d ' ' -f 1 > subdomains_$target_alive.txt
	echo "[+] Alive domains saved in 'subdomains_$target_alive.txt' file"
