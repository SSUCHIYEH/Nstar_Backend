from fastapi import HTTPException, status
from router.schemas import ProductRequestSchema
from sqlalchemy import func
from sqlalchemy.orm.session import Session
from .products_feed import products

from db.models import Product


def db_feed(db: Session):
    new_product_list = [Product(
        category=product["category"],
        name=product["name"],
        price=product["price"],
        image=product["image"],
        size=product["size"],
        color=product["color"],
        tag=product["tag"],
        description=product["description"],
        owner_id=product["owner_id"]
    ) for product in products]
    db.query(Product).delete()
    db.commit()
    db.add_all(new_product_list)
    db.commit()
    return db.query(Product).all()


def create(db: Session, request: ProductRequestSchema) -> Product:
    new_product = Product(
        category=request.category,
        name=request.name,
        price=request.price,
        image=request.image,
        size=request.size,
        color=request.color,
        tag=request.tag,
        description=request.description,
        owner_id=request.owner_id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_all(db: Session) -> list[Product]:
    return db.query(Product).all()


def get_product_by_id(product_id: int, db: Session) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id = {product_id} not found')
    return product


def get_product_by_category(category: str, db: Session) -> list[Product]:
    product = db.query(Product).filter(func.upper(Product.category) == category.upper()).all()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with category = {category} not found')
    return product

def delete_product_by_id(product_id:int, db:Session) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id = {product_id} not found')
    db.delete(product)
    db.commit()
    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=f'Product with id = {product_id} delete')