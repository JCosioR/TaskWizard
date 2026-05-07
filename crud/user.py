from sqlalchemy.orm import Session
from db.models import UserDB
from schemas.user import UserCreate

def create_user(user_in: UserCreate, db: Session):
    user_data = user_in.model_dump()

    db_user = UserDB(
        email=user_data["email"],
        full_name=user_data.get("full_name"),
        password=user_data["password"] + "_fakehashed",  # luego trabajo en esto
        is_active=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: int, db: Session):
    return db.query(UserDB).filter(UserDB.id == user_id).first()

def get_user_list(db: Session):
    return db.query(UserDB).all()

def update_user(db_user, user_up, db: Session):
    user_data = user_up.model_dump()
    db_user.email = user_data["email"]
    db_user.full_name = user_data["full_name"]
    db_user.password = user_data["password"] + "_fakehashed"
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db_user, db: Session):
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

def get_user_by_emaiil(user_email, db: Session):
    return db.query(UserDB).filter(UserDB.email == user_email).first() is not None