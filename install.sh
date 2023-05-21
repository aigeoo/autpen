go install -v github.com/owasp-amass/amass/v3/...@master

go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

go install github.com/tomnomnom/assetfinder@latest

go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

cd /vendor && git clone https://github.com/aboul3la/Sublist3r.git & cd Sublist3r && pip install -r requirements.txt

cd /vendor && git clone https://github.com/guelfoweb/knock.git && cd knock && python setup.py install
