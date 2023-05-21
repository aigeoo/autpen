#!/bin/bash

# Install required tools
echo "[+] Installing subfinder"
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

echo "[+] Installing assetfinder"
go install github.com/tomnomnom/assetfinder@latest

echo "[+] Installing sublist3r"
git clone https://github.com/aboul3la/Sublist3r.git
cd Sublist3r && pip install -r requirements.txt

echo "[+] Installing knockpy"
git clone https://github.com/guelfoweb/knock.git
cd knock && sudo python setup.py install

echo "[+] Installing massdns"
git clone https://github.com/blechschmidt/massdns.git
cd massdns && make && cp bin/massdns /usr/bin/

echo "[+] Installing httpx"
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

echo "[+] All tools installed successfully!"
