# Define una instancia app = FastAPI() y una ruta básica
from fastapi import FastAPI, Depends
from schemas.user import User, UserCreate
from db.session import get_db
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hola Mundo"}

# Read (GET)
@app.get("/users/test")
def read_user():
    return {"user": "test"}

# Receive email, full_name, id, is_active
@app.post("/register")
async def create_user(user: UserCreate):
    new_user = user
    return new_user

#@app.post("/users/")    # esto va en db.session.py?
#async def create_user():
#    db = SessionLocal()
#    db_user = User
#    db.add(db_user)
#    db.commit()
#    db.refresh(db_user)
#    return db_user

# Create (Create) // esto está en main
@app.post("/register_new")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # db es la sesión de SQLAlchemy que se va a usar
    # Se simula el guardado
    print(f"Guardando a {user.full_name} en la DB")
    return {"message": "Usuario recibido", "db_status": "Connected"}

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