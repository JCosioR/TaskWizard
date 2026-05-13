from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLAlchemy models
# podra ser necesario normalizar el imput a lowercase
# para validar el input de email se usara pydantic
class Tenant(Base):
    __tablename__= "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True) 
    full_name =  Column(String, index=True)
    password = Column(String)
    is_active = Column(Boolean, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))