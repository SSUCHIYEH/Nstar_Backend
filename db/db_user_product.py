from fastapi import HTTPException, status
from router.schemas import ProductRequestSchema, UserLikeCollectSchema
from sqlalchemy.orm.session import Session
from sqlalchemy import func, exc
from sqlalchemy.exc import IntegrityError
from db.models import User, Product, Like
import uuid


def create_user_sellproduct(user_id: int, request: ProductRequestSchema, db: Session) -> User:
    db_item = Product(
        category=request.category,
        name=request.name,
        price=request.price,
        image=request.image,
        description=request.description,
        owner_id=user_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_user_likecollect_by_id(user_id: int, request: UserLikeCollectSchema, db: Session) -> User:
    # product = Product(
    #     category=request.category,
    #     name=request.name,
    #     price=request.price,
    #     image=request.image,
    #     description=request.description,
    #     owner_id=request.owner_id
    # )
    db_like = Like(
        # product=product,
        product_id=request.product_id,
        liker_id=user_id
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like