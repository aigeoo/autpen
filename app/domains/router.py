from fastapi import APIRouter, HTTPException, status
from app.domains.utils import enumerate_subdomains
from app.database import db
from app.domains.schema import DomainModel, UpdateDomainModel
import requests, json, datetime, asyncio
from bson import ObjectId

router = APIRouter(
    prefix = "/domains",
    tags = ["domains"],
)

async def enumerate_and_insert(domain: str) -> None:
    domains = enumerate_subdomains(domain)
    main = domain
    last_update = str(datetime.datetime.utcnow())
    total = len(domains)

    the_object = {
        "main": main,
        "domains": domains,
        "last_update": last_update,
        "total": total
    }

    await db.domains.insert_one(the_object)

async def enumerate_and_update(domain: str) -> None:
    domains = enumerate_subdomains(domain)
    last_update = str(datetime.datetime.utcnow())
    total = len(domains)

    update_object = {
        "$set": {
            "domains": domains,
            "last_update": last_update,
            "total": total
        }
    }

    await db.domains.update_one({"main": domain}, update_object)

# A custom JSONEncoder to handle ObjectId objects in mongodb
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@router.get(
    "/",
    response_description="List all exsisting domains",
    status_code=status.HTTP_200_OK
)
async def index():
    """
    List all of the exsisting domains in the database

    Returns:
    --------
    json: A json representing all of the domains which is stored in the database

    """
    domains_cursor = db.domains.find({}, {"_id": 0})
    domains = await domains_cursor.to_list(None)

    return json.loads(JSONEncoder().encode(domains))

@router.post(
    "/{domain}",
    response_description="Store a new domain",
    status_code=status.HTTP_201_CREATED
)
async def store(domain: str):
    """
    Store a new domain in the database

    Paramerters:
    ------------
    domain(str): A string representing the domain name

    Returns:
    --------
    json: A json representing a message tells the user to wait until the process gets finished.

    """
    existing_record = await db.domains.find_one({"main": domain})

    if existing_record:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"The domain is already exsists"
            )

    asyncio.create_task(enumerate_and_insert(domain))

    return {"message": "This process will take approximately 5 minutes to view results go to /domains endpoint"}

@router.get(
    "/{domain}",
    response_description="Show a single domain",
    status_code=status.HTTP_200_OK
)
async def show(domain: str):
    """
    Show a single domain with all of its properties and subdomains

    Paramerters:
    ------------
    domain(str): A string representing the domain name

    Returns:
    --------
    json: A json representing the domain with all its properties and subdomains

    """
    domains_cursor = db.domains.find({"main": domain}, {"_id": 0})

    if not domains_cursor:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"There's no domain with that name"
            )

    domains = await domains_cursor.to_list(None)

    return json.loads(JSONEncoder().encode(domains))

@router.put(
    "/{domain}",
    response_description="Update a single domain",
    status_code=status.HTTP_200_OK
)
async def update(domain: str):
    """
    Update a single domain with all of its properties and subdomains

    Paramerters:
    ------------
    domain(str): A string representing the domain name

    Returns:
    --------
    json: A json representing the message to user of the process status

    """
    existing_record = await db.domains.find_one({"main": domain})

    if existing_record:
        asyncio.create_task(enumerate_and_update(domain))
        return {"message": "This process will take approximately 5 minutes to view results go to /domains endpoint"}

    raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"The domain is not exsisted in the database"
            )

@router.delete(
    "/{domain}",
    response_description="Delete a single domain",
    status_code=status.HTTP_200_OK
)
async def destroy(domain: str):
    """
    Delete a single domain with all of its properties and subdomains

    Paramerters:
    ------------
    domain(str): A string representing the domain name

    Returns:
    --------
    json: A json representing the message to user of the process status

    """
    await db.domains.delete_one({"main": domain})

    return {"message": "The domain was deleted successfully"}