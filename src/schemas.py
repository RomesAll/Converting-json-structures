from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from models import Workload

class PaginationParams(BaseModel):
    limit: int = Field(100, ge=0, le=100, description='Кол-во выводимых записей')
    offset: int = Field(0, ge=0, description='Смещение')

class ParamsForSelectDef(BaseModel):
    model_orm: object

class ParamsForSelect(ParamsForSelectDef):
    model_orm_rel_var: object
    type_load: object

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

class ResumesAddDTO(BaseModel):
    title: str
    compensation: Optional[int] = None
    workload: Workload
    worker_id: int

    def get_attrs(self):
        return {
            'title': self.title,
            'compensation': self.compensation,
            'workload': self.workload,
            'worker_id': self.worker_id
        }

class ResumesDTO(ResumesAddDTO):
    id: int
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
    
class WorkerRelDTO(WorkerDTO):
    resumes: list["ResumesDTO"]

    def get_attrs(self):
        dict = super().get_attrs()
        dict.update({'resumes': self.resumes})
        return dict