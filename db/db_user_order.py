from fastapi import HTTPException, status
from  router.schemas import CreateOrderBuyRequestSchema
from sqlalchemy.orm.session import Session
from sqlalchemy import func, exc
from sqlalchemy.exc import IntegrityError
from db.models import User, Product_sale, Order
import uuid


def create_order(user_buy_id:int,request: CreateOrderBuyRequestSchema,db:Session):
    id = uuid.uuid4()
    try:
        new_order = Order(
            id=str(id),
            finish=False,
            payment=request.payment,
            address=request.address,
            totalprice=request.totalprice,
            user_buy_id=user_buy_id,
            user_sell_id=request.user_sell_id
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        order_id = new_order.id
        new_oerder_item = [Product_sale(
            order_id=order_id,
            category=item.category,
            name=item.name,
            size=item.size,
            color=item.color,
            tag=item.tag,
            price=item.price,
            image=item.image,
            description=item.description
        )for item in request.product_items]
        db.add_all(new_oerder_item)
        db.commit()
        order = db.query(Order).filter(Order.id == order_id).first()
        order_items = db.query(Product_sale).filter(Product_sale.order_id == order_id).all()

        return {
            "id": order.id,
            "product_items": order_items,
            "payment": order.payment,
            "address": order.address,
            "totalprice": order.totalprice,
            "user_buy_id": order.user_buy_id,
            "user_sell_id": order.user_sell_id
        }


    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"{exc}".split('\n')[0])


def get_user_order_by_id(user_id:int ,db:Session):
    user = db.query(User).filter(
        User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id = {user_id} not found')
    return user