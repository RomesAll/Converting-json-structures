from repository import *
from schemas import *
from models import *
from sqlalchemy.orm import joinedload, lazyload, selectinload

class DefaultCRUDService:

    @staticmethod
    async def service_select_workers_rel() -> WorkerRelDTO:
        orm_model = await DefaultDAO.select_all_data_form_db(WorkersORM, selectinload, WorkersORM.resumes)
        dto_model = [WorkerRelDTO.model_validate(row, from_attributes=True) for row in orm_model]
        return dto_model

    @staticmethod
    async def service_select_resumes_rel() -> ResumesRelDTO:
        orm_model = await DefaultDAO.select_all_data_form_db(ResumesORM, joinedload, ResumesORM.worker)
        dto_model = [ResumesRelDTO.model_validate(row, from_attributes=True) for row in orm_model]
        return dto_model
    
    @staticmethod
    async def service_select_workers() -> WorkerDTO:
        orm_model = await DefaultDAO.select_all_data_form_db(WorkersORM)
        dto_model = [WorkerDTO.model_validate(row, from_attributes=True) for row in orm_model]
        return dto_model

    @staticmethod
    async def service_select_resumes() -> ResumesDTO:
        orm_model = await DefaultDAO.select_all_data_form_db(ResumesORM)
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

asyncio.run(DefaultCRUDService.service_update_workers(
    WorkerDTO(
        id=3,
        first_name='zzz',
        phone='32423'
    )
))