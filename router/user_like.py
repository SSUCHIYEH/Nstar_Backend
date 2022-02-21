from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from router.schemas import UserResponseWithLikeProductSchema, UserLikeCollectSchema
from db.database import get_db
from db import db_user_like, db_user


router = APIRouter(
    prefix='/api/v1/user-like',
    tags=['UserLike']
)


# 查詢我的收藏
@router.get('/like-collect/{user_id}', response_model=UserResponseWithLikeProductSchema)
def get_user_like_by_id(user_id: int, db: Session = Depends(get_db)):
    return db_user.get_user_by_id(user_id=user_id, db=db)


# 新增收藏
@router.put('/create-like-collect/{user_id}')
def create_likecollect_by_id(user_id: int, request: UserLikeCollectSchema, db: Session = Depends(get_db)):
    return db_user_like.create_user_likecollect_by_id(user_id=user_id, request=request, db=db)


@router.get('/delete-like-collect/{product_id}')
def delete_like_by_id(product_id: int, db: Session = Depends(get_db)):
    return db_user_like.delete_like_by_id(product_id=product_id, db=db)