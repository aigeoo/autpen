import re, json, subprocess, os

domains = []

def knock(domain):
    subprocess.run(['python3', f'C:\\Users\\User\\Desktop\\projects\\python\\autpen\\vendor\\knock\\knockpy.py', '--no-http', domain, '--silent'])

    # reports = os.listdir(os.getcwd() + '/vendor/knock/knockpy_report/')

    # if reports:
    #     with open(reports[0]) as f:
    #         data = json.load(f)

    #     domain_regex = re.compile(r'^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$')

    #     for value in data.keys():
    #         if domain_regex.match(value) and value not in domains:
    #             domains.append(value)

    #     os.remove(reports[0])

    print(domains)

knock('hackerone')