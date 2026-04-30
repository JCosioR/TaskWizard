from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr
from db.session import get_engine

Base = declarative_base()

# SQLAlchemy models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, index=True)
    email = Column(EmailStr, unique=True, index=True)
    full_name =  Column(String, index=True)
    password = Column(String)
    is_active = Column(Boolean, index=True)

engine = get_engine()
Base.metadata.create_all(bind=engine)