def checking_variables_db(funct):
    def wrapper(*args, **kwargs):
        params = args[0].get_dict_attributes
        if all(params.values()):
            return funct(*args, **kwargs)
        return args[0].DATABASE_DEFAULT_URL
    return wrapper