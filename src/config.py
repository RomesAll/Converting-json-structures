from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from decorators import checking_variables_db


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file="dev.env")

class DataBase(ConfigBase):    
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: Optional[int] = None
    POSTGRES_MODE: Optional[str] = None

    @property
    def get_dict_attributes(self):
        return self.__dict__

    @property
    @checking_variables_db
    def DATABASE_URL_async(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    @checking_variables_db
    def DATABASE_URL_sync(self):
        return f'postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def DATABASE_DEFAULT_URL(self):
        return f'sqlite+pysqlite:///:default.db:'

class Settings(BaseSettings):
    database: DataBase = DataBase()

settings = Settings()