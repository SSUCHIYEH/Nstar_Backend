from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from router.schemas import UserRequestSchema, UserResponseSchema, UserSignInResponseSchema
from router.schemas import SignInRequestSchema, UpdateRequestSchema
from db.database import get_db
from db import db_user
from typing import List
from utils.oauth2 import get_current_user, get_current_user_with_id

router = APIRouter(
    prefix='/api/v1/users',
    tags=['User']
)


@router.post('')
async def create(request: UserRequestSchema, db: Session = Depends(get_db)):
    return db_user.create(db=db, request=request)


@router.post('/user/register', response_model=UserSignInResponseSchema)
async def register(request: UserRequestSchema, db: Session = Depends(get_db)):
    return db_user.register(db=db, request=request)


@router.post('/user/signin', response_model=UserSignInResponseSchema)
async def signin(request: SignInRequestSchema, db: Session = Depends(get_db)):
    return db_user.signin(db=db, request=request)


@router.put('/user/update')
def update_user(request: UpdateRequestSchema, db: Session = Depends(get_db),
                current_user: UserRequestSchema =
                Depends(get_current_user)):
    return db_user.update(db=db, request=request)


@router.get('/email/{user_email}', response_model=UserResponseSchema)
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
    return db_user.get_user_by_email(user_email=user_email, db=db)


@router.get('/user/all-user', response_model=List[UserResponseSchema])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)


@router.get('/user-info/{user_id}', response_model=UserResponseSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return db_user.get_user_by_id(user_id=user_id, db=db)


