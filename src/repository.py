from database import async_session_factory
from sqlalchemy import select
from decorators import checking_type_load
from models import WorkersORM
from schemas import *
import asyncio

class DefaultDAO:

    @classmethod
    async def select_all_data_form_db(cls, select_params: SelectParams, pagination_params: PaginationParams):
        async with async_session_factory() as session:
            query = await cls._query_builder(select_params=select_params, pagination_params=pagination_params)
            res_query = await session.execute(query)
            orm_objects = res_query.scalars().all()
            return orm_objects
    
    @classmethod
    async def insert_data_from_db(cls, model_orm_new_data):
        async with async_session_factory() as session:
            session.add(model_orm_new_data)
            await session.flush()
            result = model_orm_new_data.id
            await session.commit()
            return result

    @classmethod
    async def update_data_from_db(cls, model_orm_new_data):
        async with async_session_factory() as session:
            model_orm_old_data = await session.get(model_orm_new_data.__class__, model_orm_new_data.id)
            await session.refresh(model_orm_old_data)
            await DefaultDAO._update_attrs(model_orm_old_data, model_orm_new_data)
            await session.commit()
            return id
    
    @classmethod
    async def delete_data_from_db(cls, id: int, model_orm_name):
        async with async_session_factory() as session:
            delete_object = await session.get(model_orm_name, id)
            if delete_object:
                await session.delete(delete_object)
            await session.commit()
            return id
        
    @staticmethod
    async def _update_attrs(old_data: object, new_data: object):
        old_data_attrs_key = old_data.__dict__.keys()
        new_data_attrs_items = new_data.__dict__.items()
        new_data_dict = new_data.__dict__
        old_data_dict = old_data.__dict__

        for k, v in new_data_attrs_items:
            if k != '_sa_instance_state' and k in old_data_attrs_key and new_data_dict[k] != old_data_dict[k] and new_data_dict[k]:
                setattr(old_data, k, v)
    
    @staticmethod
    @checking_type_load
    async def _query_builder(select_params: SelectParams, pagination_params: PaginationParams):
        model_orm = select_params.model_orm
        rel_var = select_params.model_orm_rel_var
        type_load_rel_var = select_params.type_load
        limit = pagination_params.limit
        offset = pagination_params.offset
        
        query = select(model_orm)

        if rel_var and type_load_rel_var:
            query = query.options(type_load_rel_var(rel_var))
        
        if limit != None and offset != None:
            query = query.limit(limit).offset(offset)
        
        return query