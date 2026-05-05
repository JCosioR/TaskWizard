# En este programa se integrará el endpoint con base de datos de manera resuimda
    # El siguiente snippet se coloca en main.py.
from fastapi import FastAPI, Depends, HTTPException, status # main.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean   # main.py, db.models.py
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr    # schemas.user.py
from sqlalchemy.orm import Session, sessionmaker  # main.py, db.session.py

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test2.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

    # El siguiente snippet se coloca en db.models.py
Base = declarative_base()



"""
Hasta aquí es posible declarar y crear la base de datos con solo imports y sin
llamadas entre funciones en scripts separados. En este ejercicio todo se manejará
dentro del mismo script.
"""

    # Definiremos las clases de User para después volver a main.py
    # y llamar UserCreate en el endpoint.
        # En este punto encontré una redundancia en session.py, que
        # aparentemente es la base de datos que sí se está utilizando.
        # Revisar luego

    # El siguiente snippet se coloca en schemas.user.py
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

# Solo para responder (devuelve el ID pero NO la contraseña)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

    # El siguiente snippet se coloca en db.session.py
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    # El siguiente snippet se coloca en db.models.py
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), index=True)
    password = Column(String)
    is_active = Column(Boolean, index=True)

    # Volvemos a main.py # lo había colocado antes de crear la clase pero por algún motivo que aún no entiendo,
    # se debe colocar después (creo que lo más limpio es colocar las clases hasta arriba, luego las funciones y
    # al)
Base.metadata.create_all(bind=engine)

    # El siguiente snippet se coloca en crud.user.py
def create_user(user_in: UserCreate, db: Session):
    user_data = user_in.model_dump()

    db_user = UserDB(
        email=user_data["email"],
        full_name = user_data.get("full_name"),
        password=user_data["password"] + "hash",
        is_active=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(id:int, db: Session):
    return db.query(UserDB).filter(UserDB.id == id).first()

    # Volvemos a main.py
@app.post("/register", response_model=UserResponse)
def create_user_endpoint(user_in: UserCreate, db: Session = Depends(get_db)):
    return create_user(user_in=user_in, db=db)

@app.get("/users/{id}", response_model=UserResponse)
def get_user_endpoint(id:int, db: Session = Depends(get_db)):
    db_user = get_user(id, db)
    
    # 2. Validamos si el resultado es None
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return db_user