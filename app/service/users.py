from sqlalchemy.orm import Session
from app.schemas import UsersResponse
from fastapi import HTTPException
from app.repository import users as user_repository


def create_user(db: Session, login: str) -> UsersResponse:
    # Проверить, существует ли такой логин
    if user_repository.get_user(db=db, login=login):
        raise HTTPException(
            status_code=400,
            detail=f"User already exists"
        )
    user = user_repository.create_user(db=db, login=login)
    db.commit()
    return UsersResponse.model_validate(user)


