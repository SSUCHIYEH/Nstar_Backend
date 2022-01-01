from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from router.schemas import UserRequestSchema, UserResponseSchema, \
    UserResponseWithProductsSchema, UserLikeCollectSchema, UserResponseWithLikeProductSchema
from router.schemas import ProductRequestSchema, CreateOrderBuyResponseSchema, CreateOrderBuyRequestSchema
from router.schemas import UserResponseWithOrderBuySchema, UserResponseWithOrderSellSchema
from db.database import get_db
from db import db_user_product, db_user
from typing import List

router = APIRouter(
    prefix='/api/v1/user-product',
    tags=['UserProduct']
)


# 查詢我的商品
@router.get('/my-product/{user_id}', response_model=UserResponseWithProductsSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return db_user.get_user_by_id(user_id=user_id, db=db)


# 創建我的商品
@router.put('/create-my-product/{user_id}')
def create_sellproduct(user_id: int, request: ProductRequestSchema, db: Session = Depends(get_db)):
    return db_user_product.create_user_sellproduct(user_id=user_id, request=request, db=db)


# 查詢我的收藏
@router.get('/like-collect/{user_id}', response_model=UserResponseWithLikeProductSchema)
def get_user_like_by_id(user_id: int, db: Session = Depends(get_db)):
    return db_user.get_user_by_id(user_id=user_id, db=db)


# 新增收藏
@router.put('/create-like-collect/{user_id}')
def create_likecollect_by_id(user_id: int, request: UserLikeCollectSchema, db: Session = Depends(get_db)):
    return db_user_product.create_user_likecollect_by_id(user_id=user_id, request=request, db=db)


