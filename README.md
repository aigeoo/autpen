# autpen
autpen is a penetration testing automation tool is a comprehensive solution that includes various features, including efficient subdomain enumeration capabilities

## installation:
1. clone the repository.
2. Run `cd autpen`
3. Create `.env` file from `.env.example` file
4. Run `chmod +x install.sh && ./install.sh`
5. Run `uvicorn app.main:app --host 127.0.0.1 --port 8000`
6. Browse `127.0.0.1:8000/`

## installation using Docker:
```
docker-compose up --build
```

---
# Endpoints

HTTP Request | Endpoint | Notes
| :---: | :---: | :---:
POST   | ```/{domain}```                  | Create new record
GET    | ```/domains/```                  | Retrieve all the stored domains
GET    | ```/domains/{domain}```          | Retrieve all stored data for a single domain
PUT    | ```/domains/{domain}```          | Update a domain's data
DELETE | ```/pdf/delete/{id}```           | Delete a domain and any related data
GET    | ```/```                          | Returns a greeting statment
