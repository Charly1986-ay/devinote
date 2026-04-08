from pydantic import ConfigDict
from sqlmodel import  SQLModel, Field, Table


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str = Field(default='')
    hashed_password = str


class UserCreate(SQLModel):   
    email: str
    full_name: str = ''
    hashed_password = str


class UserRead(SQLModel):
    id: int
    email: str
    full_name: str 
    model_config = ConfigDict(from_attributes=True)