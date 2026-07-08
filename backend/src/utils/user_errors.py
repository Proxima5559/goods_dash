from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: str):
        super().__init__(status_code=404, detail=f"User with ID {user_id} not found")


class OrderNotFoundException(HTTPException):
    def __init__(self, order_id: str):
        super().__init__(status_code=404, detail=f"Order with ID {order_id} not found")


class ProductNotFoundException(HTTPException):
    def __init__(self, product_id: str):
        super().__init__(status_code=404, detail=f"Product with ID {product_id} not found")