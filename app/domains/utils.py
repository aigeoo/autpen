import re, json, subprocess, os

VENDOR_PATH = os.getcwd() + '/vendor'
domains = []

def sublist3r(domain: str) -> None:
    """
    Use Sublist3r to eumerate subdomains

    Parameters:
    -----------
    domain(str): A string representing the domain name

    """
    output_file = os.getcwd() + '/subdomains.txt'

    subprocess.run(['touch', 'subdomains.txt'])

    subprocess.run(['python3', f'{VENDOR_PATH}/Sublist3r/sublist3r.py', '-d', domain, '-t', '5', '-o', output_file])

    save_and_delete(output_file)

def knock(domain: str) -> None:
    """
    Use Knockpy to eumerate subdomains

    Parameters:
    -----------
    domain(str): A string representing the domain name

    """
    subprocess.run(['python3', f'{VENDOR_PATH}/knock/knockpy.py', domain, '--no-local'])

    reports = os.listdir(os.getcwd() + '/knockpy_report/')

    if reports:
        with open(os.getcwd() + '/knockpy_report/' + reports[-1]) as f:
            data = json.load(f)

        domain_regex = re.compile(r'^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$')

        for value in data.keys():
            if domain_regex.match(value) and value not in domains:
                domains.append(value.replace('\n', ''))

        os.system(f'rm -rf {os.getcwd()}/knockpy_report/')

def assetfinder(domain: str) -> None:
    """
    Use Assetfinder to eumerate subdomains

    Parameters:
    -----------
    domain(str): A string representing the domain name

    """
    output_file = os.getcwd() + '/assetfinder.txt'

    subprocess.run(['touch', output_file])

    os.system(f'assetfinder --subs-only {domain} > {output_file}')

    save_and_delete(output_file)

def subfinder(domain: str) -> None:
    """
    Use Subfinder to eumerate subdomains

    Parameters:
    -----------
    domain(str): A string representing the domain name

    """
    output_file = os.getcwd() + '/subfinder.txt'

    subprocess.run(['touch', output_file])

    os.system(f'subfinder -d {domain} -silent > {output_file}')

    save_and_delete(output_file)

def amass(domain: str) -> None:
    """
    Use Amass to eumerate subdomains

    Parameters:
    -----------
    domain(str): A string representing the domain name

    """
    output_file = os.getcwd() + '/amass.txt'

    subprocess.run(['touch', output_file])

    os.system(f'amass enum -o {output_file} -passive -d {domain}')

    save_and_delete(output_file)

def httpx(domains: list[str]) -> None:
    """
    Use httpx to unsure that all subdomains are worikng

    Parameters:
    -----------
    domains(List[str]): An array representing all of the subdomains

    """
    test_file = os.getcwd() + '/test.txt'

    subprocess.run(['touch', test_file])

    with open(test_file, "w") as txt_file:
        for line in domains:
            txt_file.write("".join(line) + "\n")

    domains = []

    output_file = os.getcwd() + '/alive.txt'

    subprocess.run(['touch', output_file])

    os.system(f'httpx -l {test_file} -silent -timeout 20 -o {output_file}')

    with open(output_file) as f:
        for value in f.readlines():
            if value not in domains:
                domains.append(value.replace('\n', ''))

    os.system(f'rm -rf {test_file}')
    os.system(f'rm -rf {output_file}')

def save_and_delete(file: str) -> None:
    """
    Append the file contents to an array, then delete it 

    Parameters:
    -----------
    file(str): A string representing the path of the file

    """
    domain_regex = re.compile(r'^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$')

    with open(file) as f:
        for value in f.readlines():
            if domain_regex.match(value) and value not in domains:
                domains.append(value.replace('\n', ''))

    os.system(f'rm -rf {file}')

def enumerate_subdomains(domain: str) -> list[str]:
    assetfinder(domain)
    subfinder(domain)
    knock(domain)
    sublist3r(domain)
    # amass(domain)
    httpx(domains)

    return domains
