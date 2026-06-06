# schemas.tenant.py
from pydantic import BaseModel, EmailStr

class TenantCreate(BaseModel):
    name: str
    
class Tenant(TenantCreate):
    id: int

    class Config:
        from_attributes = True # Permite leer datos de modelos ORM -- investigar luego (doubts.md)

class TenantResponse(TenantBase):
    id: int
    
    class Config:
        from_attributes = True