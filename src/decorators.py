from sqlalchemy.orm import lazyload, selectinload, joinedload
from pydantic import ValidationError

def checking_variables_db(funct):
    def wrapper(*args, **kwargs):
        params = args[0].get_dict_attributes
        if all(params.values()):
            return funct(*args, **kwargs)
        return args[0].DATABASE_DEFAULT_URL
    return wrapper

def checking_type_load(funct):
    def wrapper(*args, **kwargs):
        type_load = None

        a = kwargs

        #Если type_load находиться в позиционных аргументах
        for i in range(len(args)):
            current_arg = args[i].__dict__.get('type_load', None)
            if current_arg and current_arg in [selectinload, lazyload, joinedload]:
                type_load = current_arg
                break
        
        #Если type_load находиться в именованных аргументах
        if not type_load and kwargs.get('select_params', None):
            select_params = kwargs.get('select_params')
            if select_params.__dict__.get('type_load', None):
                type_load = select_params.__dict__.get('type_load')
        
        if type_load == lazyload:
            raise ValueError('В асинхронных методах нельзя использовать ленивую загрузку')
        return funct(*args, **kwargs)
    return wrapper