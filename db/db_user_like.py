from fastapi import HTTPException, status
from router.schemas import UserLikeCollectSchema
from sqlalchemy.orm.session import Session
from db.models import User, Like


def create_user_likecollect_by_id(user_id: int, request: UserLikeCollectSchema, db: Session) -> User:
    db_like = Like(
        product_id=request.product_id,
        liker_id=user_id
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def delete_like_by_id(product_id: int, db: Session):
    like = db.query(Like).filter(Like.product_id == product_id).first()
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id = {product_id} not found')
    db.delete(like)
    db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=f'Product with id = {product_id} delete')