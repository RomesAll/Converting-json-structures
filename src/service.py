from repository import *
from schemas import *
from models import *
from sqlalchemy.orm import joinedload, lazyload, selectinload
from fastapi import Depends

SelectParamsDep = Annotated[SelectParams, Depends(SelectParams)]

class DefaultCRUDService:

    @staticmethod
    async def service_select_workers_rel(pagination_params: PaginationParams) -> WorkerRelDTO:
        select_params = SelectParams(
            
            model_orm = WorkersORM, 
            model_orm_rel_var = WorkersORM.resumes, 
            type_load = selectinload

        )
        orm_model = await DefaultDAO.select_all_data_form_db(select_params, pagination_params)
        dto_model = [WorkerRelDTO.model_validate(row, from_attributes=True) for row in orm_model]
        return dto_model

    @staticmethod
    async def service_select_resumes_rel(pagination_params: PaginationParams) -> ResumesRelDTO:
        select_params = SelectParams(
            
            model_orm = ResumesORM, 
            model_orm_rel_var = ResumesORM.worker, 
            type_load = joinedload

        )
        orm_model = await DefaultDAO.select_all_data_form_db(select_params, pagination_params)
        dto_model = [ResumesRelDTO.model_validate(row, from_attributes=True) for row in orm_model]
        return dto_model
    
    @staticmethod
    async def service_select_workers(pagination_params: PaginationParams) -> WorkerDTO:
        select_params = SelectParams(model_orm = WorkersORM)
        orm_model = await DefaultDAO.select_all_data_form_db(select_params, pagination_params)
        dto_model = [WorkerDTO.model_validate(row, from_attributes=True) for row in orm_model]
        return dto_model

    @staticmethod
    async def service_select_resumes(pagination_params: PaginationParams) -> ResumesDTO:
        select_params = SelectParams(model_orm = ResumesORM)
        orm_model = await DefaultDAO.select_all_data_form_db(select_params, pagination_params)
        dto_model = [ResumesDTO.model_validate(row, from_attributes=True) for row in orm_model]
        return dto_model

    @staticmethod
    async def service_insert_workers(dto_model: WorkerAddDTO):
        orm_model = WorkersORM(**dto_model.get_attrs())
        res = await DefaultDAO.insert_data_from_db(orm_model)
        return res

    @staticmethod
    async def service_insert_resumes(dto_model: ResumesAddDTO):
        orm_model = ResumesORM(**dto_model.get_attrs())
        res = await DefaultDAO.insert_data_from_db(orm_model)
        return res
    
    @staticmethod
    async def service_update_workers(dto_model: WorkerDTO):
        orm_model = WorkersORM(**dto_model.get_attrs())
        res = await DefaultDAO.update_data_from_db(orm_model)
        return res

    @staticmethod
    async def service_update_resumes(id:int, dto_model: ResumesDTO):
        orm_model = ResumesORM(**dto_model.get_attrs())
        res = await DefaultDAO.update_data_from_db(id, orm_model)
        return res

    @staticmethod
    async def service_delete_workers(id:int):
        res = await DefaultDAO.delete_data_from_db(id, WorkersORM)
        return res
      
    @staticmethod
    async def service_delete_resumes(id:int):
        res = await DefaultDAO.delete_data_from_db(id, ResumesORM)
        return res