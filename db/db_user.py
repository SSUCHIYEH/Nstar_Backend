from fastapi import HTTPException, status
from router.schemas import UserRequestSchema
from sqlalchemy.orm.session import Session
from sqlalchemy import func, exc
from sqlalchemy.exc import IntegrityError
from db.models import User
import uuid

def create(db: Session, request: UserRequestSchema) -> User:
    new_user = User(
        username=request.username,
        email=request.email,
        password=request.password,
        image=request.image,
        is_admin=request.is_admin,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"{exc}".split('\n')[0])


def get_all(db: Session) -> list[User]:
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Users not found')
    return users


def get_user_by_id(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id = {user_id} not found')
    return user





