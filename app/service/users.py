from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository import users as user_repository
from app.schemas import UsersResponse


def create_user(db: Session, login: str) -> UsersResponse:
    # Проверить, существует ли такой логин
    if user_repository.get_user(db=db, login=login):
        raise HTTPException(status_code=400, detail="User already exists")
    user = user_repository.create_user(db=db, login=login)
    db.commit()
    return UsersResponse.model_validate(user)
