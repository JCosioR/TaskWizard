# Define una instancia app = FastAPI() y una ruta básica
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud.user import create_user, get_user, get_user_list, update_user, delete_user, get_user_by_emaiil
from sqlalchemy import create_engine
from db.session import get_db
from db.models import Base
from schemas.user import UserCreate, UserResponse

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
Base.metadata.create_all(bind=engine)

@app.post("/tenants")
def create_tenant(tenant_in: TenantCreate, db: Session = Depends(get_db)):
    if get_tenant_by_name(tenant_in, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Tenant already exists"
        )
    return create_tenant(tenant_in=tenant_in, db=db)

@app.get("/")
def read_root():
    return {"message": "Hola Mundo"}

# Read (GET)
@app.get("/users/test")
def read_user():
    return {"user": "test"}

@app.post("/register_new", response_model=UserResponse)
def create_user_endpoint(user_in: UserCreate, db: Session = Depends(get_db)):
    # Validamos si el email ya existe
    if get_user_by_emaiil(user_in.email, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email is already registered"
        )    
    return create_user(user_in=user_in, db=db)

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(user_id, db)

    # Validamos si el resultado es None
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return db_user

@app.get("/users", response_model=list[UserResponse])
def get_user_list_endpoint(db: Session = Depends(get_db)):
    return get_user_list(db=db)

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user_up: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(user_id, db)    
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return update_user(db_user=db_user, user_up=user_up, db=db)

@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(user_id, db)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    else:
        return delete_user(db_user=db_user, db=db)



