# Define una instancia app = FastAPI() y una ruta básica
from fastapi import FastAPI, Depends
from schemas.user import User, UserCreate
from db.session import get_db
from sqlalchemy.orm import Session
from crud.user import create_user, get_user
from sqlalchemy import create_engine
from db.models import Base

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

@app.get("/users/{user_id}")
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_user(user_id=user_id, db=db)

"""
# CRUD operations
# Create (Create)
@app.post("/items/")
async def create_item(name: str, description: str):
    db = SessionLocal()
    db_item = Item(name=name, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
    """