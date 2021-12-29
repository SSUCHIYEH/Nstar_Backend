from fastapi import HTTPException, status
from router.schemas import UserRequestSchema, SignInRequestSchema, UpdateRequestSchema
from sqlalchemy.orm.session import Session
from sqlalchemy import func, exc
from sqlalchemy.exc import IntegrityError
from db.models import User
from utils.hash import bcrypt, verify
from utils.oauth2 import create_access_token
from .user_feed import users


def db_feed(db:Session):
    new_user_list = [User(
        username=user["username"],
        email=user["email"],
        image=user["image"],
        is_admin=True,
        password=user["password"]
    ) for user in users]
    db.query(User).delete()
    db.commit()
    db.add_all(new_user_list)
    db.commit()
    return db.query(User).all()

def register(db: Session, request: UserRequestSchema) :
    new_user = User(
        username=request.username,
        email=request.email,
        image=request.image,
        password=bcrypt(request.password),
        is_admin=request.is_admin,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        access_token = create_access_token(data={'username': new_user.username})

        return {
            'access_token': access_token,
            'user_id': new_user.id,
            'username': new_user.username
        }
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"{exc}".split('\n')[0])


def signin(db: Session, request: SignInRequestSchema):
    user = db.query(User).filter(func.upper(User.email) == request.email.upper()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'沒有找到 {request.email} 這組email帳號')
    if not verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='密碼不對')

    access_token = create_access_token(data={'username': user.username})

    return {
        'access_token': access_token,
        'user_id': user.id,
        'username': user.username
    }


def update(db: Session, request: UpdateRequestSchema):
    user = db.query(User).filter(User.id == request.user_id)
    user.update({
        User.username: request.username,
        User.password: bcrypt(request.password)
    })
    db.commit()
    access_token = create_access_token(data={'username': request.username})
    return {
        'access_token': access_token,
        'user_id': request.user_id,
        'username': request.username,
    }


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


def get_all_users(db: Session) -> list[User]:
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


def get_user_by_email(user_email: str, db: Session) -> User:
    user = db.query(User).filter(func.upper(User.email) == user_email.upper()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with email = {user_email} not found')
    return user


def get_user_by_username(user_name: str, db: Session) -> User:
    user = db.query(User).filter(func.upper(User.username) == user_name.upper()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with user name = {user_name} not found')
    return user
