# Define una instancia app = FastAPI() y una ruta básica
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud.user import create_user, get_user, get_user_list, update_user, delete_user
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


@app.get("/")
def read_root():
    return {"message": "Hola Mundo"}

# Read (GET)
@app.get("/users/test")
def read_user():
    return {"user": "test"}



#@app.post("/users/")    # esto va en db.session.py?
#async def create_user():
#    db = SessionLocal()
#    db_user = User
#    db.add(db_user)
#    db.commit()
#    db.refresh(db_user)
#    return db_user

@app.post("/register_new")
def create_user_endpoint(user_in: UserCreate, db: Session = Depends(get_db)):
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
    return get_user(user_id=user_id, db=db)

@app.get("/users", response_model=list[UserResponse])
def get_user_list_endpoint(db: Session = Depends(get_db)):
    return get_user_list(db=db)

@app.put("/users/{user_id}")
def update_user_endpoint(user_id: int, user_up: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(user_id, db)    
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return update_user(user_id=user_id, user_up=user_up, db=db)

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



