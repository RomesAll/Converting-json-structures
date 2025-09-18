from database import async_session_factory
from sqlalchemy import select
from decorators import checking_type_load

class DefaultDAO:

    @staticmethod
    @checking_type_load
    async def select_all_data_form_db(model_orm_name, type_load=None, var_relship=None):
        async with async_session_factory() as session:
            if type_load and var_relship:
                query = select(model_orm_name).options(type_load(var_relship))
            else:
                query = select(model_orm_name)
            res_query = await session.execute(query)
            orm_objects = res_query.scalars().all()
            return orm_objects
    
    @staticmethod
    async def insert_data_from_db(model_orm_new_data):
        async with async_session_factory() as session:
            session.add(model_orm_new_data)
            await session.flush()
            result = model_orm_new_data.id
            await session.commit()
            return result

    @staticmethod
    async def update_data_from_db(model_orm_new_data):
        async with async_session_factory() as session:
            update_object = await session.get(model_orm_new_data.__class__, model_orm_new_data.id)
            await session.refresh(update_object)
            update_object.update_attrs(model_orm_new_data)
            await session.commit()
            return id
    
    @staticmethod
    async def delete_data_from_db(id: int, model_orm_name):
        async with async_session_factory() as session:
            delete_object = await session.get(model_orm_name, id)
            if delete_object:
                await session.delete(delete_object)
            await session.commit()
            return id

