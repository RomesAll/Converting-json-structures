from pydantic import BaseModel, EmailStr, field_validator, Field, ValidationError
from typing import Optional
from datetime import datetime
from models import Workload

class WorkerAddDTO(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    phone: str
    email: Optional[EmailStr] = None

    def get_attrs(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email
        }

class WorkerDTO(WorkerAddDTO):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_attrs(self):
        dict = super().get_attrs()
        dict.update(
            {
                'id': self.id,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }
        )
        return dict

class WorkerRelDTO(WorkerDTO):
    resumes: list['ResumesDTO']

    def get_attrs(self):
        dict = super().get_attrs()
        dict.update({'resumes': self.resumes})
        return dict

class ResumesAddDTO(BaseModel):
    title: str
    compensation: Optional[int] = None
    workload: Workload
    worker_id: int

    def get_attrs(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class ResumesDTO(ResumesAddDTO):
    id: int = None
    created_at: datetime = None
    updated_at: datetime = None

    def get_attrs(self):
        dict = super().get_attrs()
        dict.update(
            {
                'id': self.id,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }
        )
        return dict

class ResumesRelDTO(ResumesDTO):
    worker: "WorkerDTO"
    
    def get_attrs(self):
        dict = super().get_attrs()
        dict.update({'worker': self.worker})
        return dict