import subprocess
import os
import sys

# check if domain is provided as an argument
if len(sys.argv) < 2:
    print(f"Usage: python3 {sys.argv[0]} [domain] (optional: subdomains file to skip first stage)")
    sys.exit(1)
else:
    target = sys.argv[1]

# check if subdomains file is provided as an argument
if len(sys.argv) < 3:
    # Get subdomains from subfinder
    subprocess.run(['subfinder', '-d', target, '-silent', '>', 'subdomains1.txt'], check=True)
    print("[+] subfinder tool result saved in subdomains1.txt")

    # Get subdomains from assetfinder
    subprocess.run(['assetfinder', target, '-subs-only', '>', 'subdomains2.txt'], check=True)
    print("[+] assetfinder tool result saved in subdomains2.txt")

    # Get subdomains from sublist3r
    subprocess.run(['sublist3r', '-n', '-d', target, '-o', 'subdomains3.txt'], check=True)
    print("[+] sublist3r tool result saved in subdomains3.txt")

    # Get subdomains from knockpy
    subprocess.run(['knockpy', '--no-http', target], check=True)
    subprocess.run(['cat', 'knockpy_report/' + target + '*', '|', 'grep', '-oP', '\'[a-z0-9]+\.' + target + '\'', '|', 'sort', '-u', '|', 'uniq', '>', 'subdomains4.txt'], check=True)
    print("[+] knockpy tool result saved in subdomains4.txt")

    # bruteforce subdomains
    subprocess.run(['awk', '-v', 'host=' + target, '{print $0"."host}', '/usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt', '>', 'massdnslist'], check=True)
    subprocess.run(['massdns', 'massdnslist', '-r', '/usr/share/seclists/Miscellaneous/dns-resolvers.txt', '-o', 'S', '-t', 'A', '-q', '|', 'awk', '-F". "', '{print $1}', '|', 'sort', '-u', '>', 'subdomains5.txt'], check=True)
    print("[+] massdns tool result saved in subdomains5.txt")

    # sort and organize the outputs
    print("[+] Sorting the result in one file 'finaldomains.txt'")
    subprocess.run(['cat', 'subdomains*.txt', '|', 'grep', '-i', target, '|', 'sort', '-u', '|', 'uniq', '>', 'allSubdomain_' + target + '.txt'], check=True)
    print("[+] Domains found: ", subprocess.run(['cat', 'allSubdomain_' + target + '.txt', '|', 'wc', '-l'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip())
    print("[+] Tool finished getting all subdomains")
    alldomains = 'allSubdomain_' + target + '.txt'
    os.system('rm -rf subdomains*.txt')
else:
    alldomains = sys.argv[2]

# Get alive domains
subprocess.run(['httpx', '-l', alldomains, '-silent', '-timeout', '20', '-title', '-tech-detect', '-status-code', '-follow-redirects', '-probe', '-o', 'subdomains_' + target + '_alive_title.txt'], check=True)
print("[+] Details of alive domains saved in 'subdomains_" + target + "_alive_title.txt' file")
os.system('cat alive_titles.txt | cut -d \' \' -f 1 > subdomains_' + target + '_alive.txt')
print("[+] Alive domains saved in 'subdomains_" + target + "_alive.txt' file")
