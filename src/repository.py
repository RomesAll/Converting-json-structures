from database import async_session_factory
from sqlalchemy import select
from sqlalchemy.orm import selectinload, lazyload
from decorators import checking_type_load
from models import WorkersORM, ResumesORM
from schemas import *
import asyncio
from typing import Union

ParamsForSelectSchema = Union[ParamsForSelectDef, ParamsForSelect]

class DefaultQueryBuilder:

    @classmethod
    async def default_select(cls, select_params: ParamsForSelectSchema):
        query = select(select_params.model_orm)
        return query
    
    @classmethod
    @checking_type_load
    async def default_select_with_rel(cls, select_params: ParamsForSelectSchema):
        if not (select_params.model_orm_rel_var and select_params.type_load):
            return None
        query = select(select_params.model_orm).options(select_params.type_load(select_params.model_orm_rel_var))
        return query

    @classmethod
    async def default_select_with_params(cls, select_params: ParamsForSelectSchema, pagination_params: PaginationParams):
        query = select(select_params.model_orm)
        if pagination_params.limit:
            query = query.limit(pagination_params.limit)
        if pagination_params.offset:
            query = query.offset(pagination_params.offset)
        return query

    @classmethod
    @checking_type_load
    async def default_select_with_params_rel(cls, select_params: ParamsForSelectSchema, pagination_params: PaginationParams):
        query = select(select_params.model_orm)
        if not (select_params.model_orm_rel_var and select_params.type_load):
            return None
        query = query.options(select_params.type_load(select_params.model_orm_rel_var))
        if pagination_params.limit:
            query = query.limit(pagination_params.limit)
        if pagination_params.offset:
            query = query.offset(pagination_params.offset)
        return query

class DefaultDAO(DefaultQueryBuilder):

    @classmethod
    async def dao_select_all_data_form_db(cls, select_params: ParamsForSelectSchema, pagination_params: PaginationParams):
        async with async_session_factory() as session:
            query = None
            if select_params.__class__ == ParamsForSelectDef:
                query = await cls.default_select_with_params(select_params, pagination_params)
            elif select_params.__class__ == ParamsForSelect:
                query = await cls.default_select_with_params_rel(select_params, pagination_params)
            res_query = await session.execute(query)
            orm_objects = res_query.scalars().all()
            return orm_objects
    
    @classmethod
    async def dao_insert_data_from_db(cls, model_orm_new_data):
        async with async_session_factory() as session:
            session.add(model_orm_new_data)
            await session.flush()
            result = model_orm_new_data.id
            await session.commit()
            return result

    @classmethod
    async def dao_update_data_from_db(cls, model_orm_new_data):
        async with async_session_factory() as session:
            model_orm_old_data = await session.get(model_orm_new_data.__class__, model_orm_new_data.id)
            await session.refresh(model_orm_old_data)
            await DefaultDAO.dao_update_attrs(model_orm_old_data, model_orm_new_data)
            await session.commit()
            return model_orm_new_data.id
    
    @classmethod
    async def dao_delete_data_from_db(cls, id: int, model_orm_name):
        async with async_session_factory() as session:
            delete_object = await session.get(model_orm_name, id)
            if delete_object:
                await session.delete(delete_object)
            await session.commit()
            return id
        
    @staticmethod
    async def dao_update_attrs(old_data: object, new_data: object):
        old_data_attrs_key = old_data.__dict__.keys()
        new_data_attrs_items = new_data.__dict__.items()
        new_data_dict = new_data.__dict__
        old_data_dict = old_data.__dict__

        for k, v in new_data_attrs_items:
            if k != '_sa_instance_state' and k in old_data_attrs_key \
                and new_data_dict[k] != old_data_dict[k] and new_data_dict[k]:
                setattr(old_data, k, v)
    
class WorkersDAO(DefaultDAO):

    @classmethod
    async def dao_select_worker_by_id(cls, id: int, select_params: ParamsForSelect) -> WorkersORM:
        async with async_session_factory() as session:
            query = (await cls.default_select_with_rel(select_params)).where(WorkersORM.id == int(id))
            res_query = await session.execute(query)
            orm_objects = res_query.scalars().all()
            return orm_objects
        
class ResumesDAO(DefaultDAO):

    @classmethod
    async def dao_select_resumes_by_id(cls, id: int, select_params: ParamsForSelect) -> ResumesORM:
        async with async_session_factory() as session:
            query = (await cls.default_select_with_rel(select_params)).where(ResumesORM.id == int(id))
            res_query = await session.execute(query)
            orm_objects = res_query.scalars().all()
            return orm_objects