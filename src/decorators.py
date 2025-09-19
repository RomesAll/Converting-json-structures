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
        for i in range(len(args)):
            if args[i] in [selectinload, lazyload, joinedload]:
                type_load = args[i]
                break
        if not type_load:
            type_load = kwargs.get("type_load", None)
        if type_load == lazyload:
            raise ValueError('В асинхронных методах нельзя использовать ленивую загрузку')
        return funct(*args, **kwargs)
    return wrapper