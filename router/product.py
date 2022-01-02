import shutil
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from router.schemas import ProductRequestSchema, ProductResponseSchema, ProductResponseWithUserSchema
from db.database import get_db
from db import db_product
from typing import List


router = APIRouter(
    prefix='/api/v1/products',
    tags=['products']
)


@router.post('', response_model=ProductResponseSchema)
def create(request: ProductRequestSchema, db: Session = Depends(get_db)):
    return db_product.create(db=db, request=request)


@router.get('/feed', response_model=List[ProductResponseSchema])
def feed_initial_products(db: Session = Depends(get_db)):
    return db_product.db_feed(db)


@router.get('/all', response_model=List[ProductResponseSchema])
def get_all_products(db: Session = Depends(get_db)):
    return db_product.get_all(db)


@router.get('/id/{product_id}', response_model=ProductResponseWithUserSchema)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return db_product.get_product_by_id(product_id=product_id, db=db)


@router.get("/category/{category}", response_model=List[ProductResponseSchema])
def get_product_by_category(category: str, db: Session = Depends(get_db)):
    return db_product.get_product_by_category(category=category, db=db)


@router.get("/delete/{product_id}")
def delete_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return db_product.delete_product_by_id(product_id=product_id, db=db)


@router.post('/image')
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return  {"file_name": file.filename}


@router.get('/image/{name}')
async def get_image(name: str):
    return  FileResponse(name,media_type="image/png")