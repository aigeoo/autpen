from fastapi import FastAPI
import requests, json

app = FastAPI()

@app.get("/domains")
async def index():

    def search_subdomains(domain):
        url = f"https://crt.sh?q=%.{domain}&output=json"

        response = requests.get(url)
        json_data = json.loads(response.text)

        subdomains = []
        for data in json_data:
            subdomain = data['name_value'].replace("*.", "")
            if subdomain not in subdomains:
                subdomains.append(subdomain)

        result = {
            "domain": domain,
            "subdomains": subdomains
        }

        return result
    
    return search_subdomains('hackerone.com')

@app.post("/domains")
async def store():
    return {"message": "Hello World"}

@app.get("/domains/{domain}")
async def show():
    return {"message": "Hello World"}


@app.put("/domains/{domain}")
async def update():
    return {"message": "Hello World"}

@app.delete("/domains/{domain}")
async def destroy():
    return {"message": "Hello World"}