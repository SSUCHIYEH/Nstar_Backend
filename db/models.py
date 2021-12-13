from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(30))
    name = Column(String(30))
    price = Column(Integer)
    size = Column(String(30))
    color = Column(String(30))
    tag = Column(String(100))
    image = Column(String(100))
    description = Column(String(100))
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User', back_populates='products_sell')


class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True, index=True)
    liker_id = Column(Integer, ForeignKey('user.id'))
    liker = relationship('User', back_populates='collects_like')
    product = relationship('Product')
    product_id = Column(Integer, ForeignKey('product.id'))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30))
    image = Column(String(100))
    email = Column(String(30), unique=True)
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)
    products_sell = relationship('Product', back_populates='owner')
    collects_like = relationship('Like', back_populates='liker')
    order_buy = relationship('Order', foreign_keys="Order.user_buy_id", back_populates='user_buy')
    order_sell = relationship('Order', foreign_keys="Order.user_sell_id", back_populates='user_sell')


class Order(Base):
    __tablename__ = 'order'
    id = Column(String, primary_key=True, nullable=False)
    finish = Column(Boolean, default=False)
    payment = Column(String(30))
    address = Column(String(100))
    totalprice = Column(Integer)
    product_items = relationship('Product_sale', back_populates='order')
    user_buy_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_sell_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_buy = relationship('User',  backref=" order_buy", foreign_keys=[user_buy_id])
    user_sell = relationship('User', backref=" order_sell", foreign_keys=[user_sell_id])
    createtime = Column(TIMESTAMP)


class Product_sale(Base):
    __tablename__ = 'product_sale'
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(30))
    name = Column(String(30))
    size = Column(String(30))
    color = Column(String(30))
    tag = Column(String(100))
    price = Column(Integer)
    image = Column(String(100))
    description = Column(String(100))
    order_id = Column(String, ForeignKey('order.id'), nullable=False)
    order = relationship('Order', back_populates='product_items', foreign_keys=[order_id])

