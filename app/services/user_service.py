from app.core.security import verify_password
from app.core.security import hash_password
from sqlalchemy.orm import Session
from app.models.user import User


def create_user(db: Session, username: str, email: str, password: str):
    hashed_password = hash_password(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session):
    return db.query(User).all()
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        db.delete(user)
        db.commit()
    
    return user
def update_user(db: Session, user_id: int, username: str, email: str):
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        user.username = username
        user.email = email
        db.commit()
        db.refresh(user)

    return user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user
