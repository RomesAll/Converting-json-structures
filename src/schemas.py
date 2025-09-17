from pydantic import BaseModel, EmailStr, field_validator, Field, ValidationError
from typing import Optional
from datetime import datetime
from models import Workload

class WorkerAddDTO(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr

class WorkerDTO(WorkerAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime

class WorkerRelDTO(WorkerDTO):
    resumes: list['ResumesDTO'] 

class ResumesAddDTO(BaseModel):
    title: str
    compensation: Optional[int]
    workload: Workload
    worker_id: int

class ResumesDTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

class ResumesRelDTO(ResumesDTO):
    worker: "WorkerDTO"