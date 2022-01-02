from router.schemas import ProductRequestSchema
from sqlalchemy.orm.session import Session
from db.models import User, Product


def create_user_sellproduct(user_id: int, request: ProductRequestSchema, db: Session) -> User:
    db_item = Product(
        category=request.category,
        name=request.name,
        price=request.price,
        image=request.image,
        tag=request.tag,
        color=request.color,
        size=request.size,
        description=request.description,
        owner_id=user_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
