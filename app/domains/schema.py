from bson import ObjectId
from typing import List, Optional
from pydantic import BaseModel, Field

class PyObjectId(ObjectId):
    """This class to handle mongodb _id"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class DomainModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    main: Optional[str]
    domains: List[str] 
    last_update: Optional[str] 
    total: Optional[int] 
    
    class Config:
        # Set default values for the fields
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "64417eea84c474232a2c9ec8",
                "domains": [
                	"support.example.com",
                	"docs.example.com",
                	"auth.example.com",
                ],
                "main": "example.com",
                "last_update": "2023-04-20 18:05:30.644889",
                "total": 34,
            }
        }

class UpdateDomainModel(BaseModel):
    domains: List[str] 
    last_update: Optional[str]
    total: Optional[int] 
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "domains": [
                	"support.example.com",
                	"docs.example.com",
                	"auth.example.com",
                ],
                "last_update": "2023-04-20 18:05:30.644889",
                "total": 34,
            }
        }