from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from router.schemas import UserRequestSchema, UserResponseSchema, \
    UserResponseWithProductsSchema, UserLikeCollectSchema, UserResponseWithLikeProductSchema
from router.schemas import ProductRequestSchema, CreateOrderBuyResponseSchema, CreateOrderBuyRequestSchema
from router.schemas import UserResponseWithOrderBuySchema, UserResponseWithOrderSellSchema
from db.database import get_db
from db import db_user
from typing import List

router = APIRouter(
    prefix='/api/v1/users',
    tags=['User']
)


@router.post('')
async def create(request: UserRequestSchema, db: Session = Depends(get_db)):
    return db_user.create(db=db, request=request)



@router.get('/all-user', response_model=List[UserResponseSchema])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all(db)


@router.get('/user-info/{user_id}', response_model=UserResponseSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return db_user.get_user_by_id(user_id=user_id, db=db)





# 創建訂單
