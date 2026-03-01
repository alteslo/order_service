from pydantic import BaseModel, ConfigDict, field_validator

from src.domain.value_objects import OrderStatus


class OrderItemRequest(BaseModel):
    """Товар в заказе (входные данные)"""
    id: int
    name: str
    quantity: int
    price: float


class OrderCreateRequest(BaseModel):
    """Схема запроса для создания заказа"""
    items: list[OrderItemRequest]

    @field_validator("items")
    @classmethod
    def items_not_empty(cls, v):
        if not v:
            raise ValueError("Список товаров не может быть пустым")
        return v


class OrderStatusUpdateRequest(BaseModel):
    """Схема запроса на обновление заказа"""
    status: OrderStatus


class OrderItemResponse(BaseModel):
    """Товар в заказе (ответ)"""
    id: int
    name: str
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    """Схема ответа для заказа"""
    id: str
    user_id: str
    items: list[OrderItemResponse]
    total_price: float
    status: OrderStatus

    model_config = ConfigDict(from_attributes=True)


class OrderListResponse(BaseModel):
    """Схема ответа для списка заказов"""
    orders: list[OrderResponse]
    total: int
