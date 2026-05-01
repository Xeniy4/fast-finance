from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database_models import User
from app.dependency import get_current_user, get_db
from app.schemas import UsersRequest, UsersResponse
from app.service import users as users_service

router = APIRouter()


@router.post("/users", response_model=UsersResponse)
def create_user(payload: UsersRequest, db: Session = Depends(get_db)):
    return users_service.create_user(db=db, login=payload.login)


@router.get("/users/me", response_model=UsersResponse)
def get_current_user(current_user: User = Depends(get_current_user)):
    return UsersResponse.model_validate(current_user)
