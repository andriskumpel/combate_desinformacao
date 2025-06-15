from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class VerificationBase(BaseModel):
    content: str
    content_type: str
    source_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class VerificationCreate(VerificationBase):
    pass

class VerificationInDB(VerificationBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    analysis_result: Optional[Dict[str, Any]] = None
    classification_result: Optional[Dict[str, Any]] = None
    status: str = "pending"
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class VerificationResponse(VerificationInDB):
    pass

class VerificationUpdate(BaseModel):
    analysis_result: Optional[Dict[str, Any]] = None
    classification_result: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow) 