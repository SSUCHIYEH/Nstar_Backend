from pydantic import BaseModel, Field, validator, EmailStr
from typing import List


# user base
class UserBase(BaseModel):
    username: str
    email: str
    image: str
    is_admin: bool


# 登入
class SignInRequestSchema(BaseModel):
    email: EmailStr
    password: str


class UpdateRequestSchema(UserBase):
    user_id: int
    username: str
    password: str


# 密碼?
class UserRequestSchema(UserBase):
    password: str

    @classmethod
    @validator("password")
    def password_must_have_6_digits(cls, v):
        if len(v) < 6:
            raise ValueError("密碼至少要超過6碼喔!")
        return v


# user
class UserResponseSchema(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserSignInResponseSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user_id: int
    username: str


# 商品詳細
class ProductRequestSchema(BaseModel):
    category: str
    name: str
    price: int
    image: str
    description: str
    owner_id: int


# 商品
class ProductResponseSchema(ProductRequestSchema):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# 商品 回user
class ProductResponseWithUserSchema(ProductRequestSchema):
    id: int
    owner_id: int
    owner: UserResponseSchema

    class Config:
        orm_mode = True


# user 回商品
class UserResponseWithProductsSchema(UserBase):
    id: int
    products_sell: List[ProductResponseSchema] = []

    class Config:
        orm_mode = True


# class likeWithProductRequestSchema(BaseModel):
#     category: str
#     name: str
#     price: int
#     image: str
#     description: str
#     owner_id: int
#     id: int

# like 商品 id
class UserLikeCollectSchema(BaseModel):
    product_id: int

    class Config:
        orm_mode = True


class UserResponseLikeCollectSchema(UserLikeCollectSchema):
    id: int

    class Config:
        orm_mode = True


# user 回 like
class UserResponseWithLikeProductSchema(BaseModel):
    id: int
    collects_like: List[UserResponseLikeCollectSchema] = []

    class Config:
        orm_mode = True


# 輸入訂單裡的商品
class SaledProductRequestSchema(BaseModel):
    category: str
    name: str
    size: str
    color: str
    tag: str
    price: int
    image: str
    description: str


# 回應商品時要有訂單號碼
class SaledProductResponseSchema(SaledProductRequestSchema):
    order_id: str


# 訂單  回應所有商品
class SaledProductResponseIDSchema(SaledProductResponseSchema):
    id: int

    class Config:
        orm_mode = True


# 創建訂單
class CreateOrderBuyRequestSchema(BaseModel):
    payment: str
    address: str
    totalprice: int
    user_sell_id: int
    user_buy_id: int
    product_items: List[SaledProductRequestSchema]


# 回應創建訂單
class CreateOrderBuyResponseSchema(BaseModel):
    id: str
    finish: bool
    payment: str
    address: str
    totalprice: int
    user_sell_id: int
    user_buy_id: int
    product_items: List[SaledProductResponseIDSchema]

    class Config:
        orm_mode = True


# order buy 詳細
class OrderBuyResponseSchema(BaseModel):
    id: str
    finish: bool
    payment: str
    address: str
    totalprice: int
    user_sell: UserResponseSchema
    product_items: List[SaledProductResponseIDSchema] = []

    class Config:
        orm_mode = True


# order sell 詳細
class OrderSellResponseSchema(BaseModel):
    id: str
    finish: bool
    payment: str
    address: str
    totalprice: int
    user_buy: UserResponseSchema
    product_items: List[SaledProductRequestSchema] = []

    class Config:
        orm_mode = True


# user 回 OrderBuy
class UserResponseWithOrderBuySchema(BaseModel):
    id: int
    order_buy: List[OrderBuyResponseSchema] = []

    class Config:
        orm_mode = True


class UserResponseWithOrderSellSchema(BaseModel):
    id: int
    order_sell: List[OrderSellResponseSchema] = []

    class Config:
        orm_mode = True


