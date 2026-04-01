from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependency import get_db
from app.service import users as users_service

from app.schemas import UsersRequest, UsersResponse

router = APIRouter()


@router.post("/users", response_model=UsersResponse)
def create_user(payload: UsersRequest, db: Session = Depends(get_db)):
    return users_service.create_user(db=db, login=payload.login)