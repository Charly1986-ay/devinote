from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Los puntitos indican que no tiene un valor por default
    DATABASE_URL: str = Field(..., env='DATABASE_URL') 
    JWT_SECRET: str = Field(..., env='JWT_SECRET')
    # tiene un valor por default
    JWT_ALG: str = Field(default='HS256', env='JWT_ALG') 
    JWT_EXPIRES_INT: int = Field(default=60*24, env='JWT_EXPIRES_INT') 
    PROJECT_NAME: str = 'Davinote'

    class Config:
        env_file = '.env'


settings = Settings()