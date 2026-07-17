from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Jaf(BaseModel):
    source_system: str 
    external_id: str
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    hire_date: date
    department: str
    city: Optional[str] = None
    state: Optional[str] = None
    status: StatusEnum