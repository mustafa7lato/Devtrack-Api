from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_current_user
from app.schemas.user import UserCreate, UserUpdate, UserLogin, UserResponse
from app.services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    delete_user,
    update_user,
    authenticate_user
)

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Welcome to DevTrack 🚀"}


@router.get("/about")
def about():
    return {"info": "Backend developer in progress"}


@router.post("/users", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user.username, user.email, user.password)


@router.get("/users", response_model=list[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return get_users(db)


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user.username, user.email)


@router.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        return {"error": "Invalid email or password"}

    access_token = create_access_token(data={"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
