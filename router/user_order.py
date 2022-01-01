from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from router.schemas import CreateOrderBuyResponseSchema, CreateOrderBuyRequestSchema
from router.schemas import UserResponseWithOrderBuySchema, UserResponseWithOrderSellSchema
from db.database import get_db
from db import db_user_order

router = APIRouter(
    prefix='/api/v1/user-order',
    tags=['UserOrder']
)


# 創建訂單
@router.post('/create-buy-order/{user_id}', response_model=CreateOrderBuyResponseSchema)
def create_order_buy_by_id(user_id: int, request: CreateOrderBuyRequestSchema, db : Session = Depends(get_db)):
    return db_user_order.create_order(user_buy_id=user_id, db=db, request=request)


# 查詢購買訂單
@router.get('/get-buy-order/{user_id}', response_model=UserResponseWithOrderBuySchema)
def get_user_buy_order_by_id(user_id: int, db: Session = Depends(get_db)):
    return db_user_order.get_user_order_by_id(user_id=user_id, db=db)


# 查詢販售訂單
@router.get('/get-sell-order/{user_id}', response_model=UserResponseWithOrderSellSchema)
def get_user_sell_order_by_id(user_id: int, db: Session = Depends(get_db)):
    return db_user_order.get_user_order_by_id(user_id=user_id, db=db)