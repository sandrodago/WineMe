from typing import List, Optional
from ...domains.products.services import ProductService
from ...domains.products.domain import ProductNotFoundException
from .dto import CreateProductRequest, UpdateProductRequest, ProductResponse

class CreateProductUseCase:
    """Use case for creating a product"""
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
    
    def execute(self, request: CreateProductRequest) -> ProductResponse:
        """Execute the create product use case"""
        try:
            product = self.product_service.create_product(
                name=request.name,
                category=request.category,
                price=request.price,
                description=request.description,
                stock_quantity=request.stock_quantity
            )
            return self._to_response(product)
        except Exception as e:
            raise e
    
    def _to_response(self, product) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name.value,
            description=product.description,
            price=product.price.value,
            category=product.category.value,
            stock_quantity=product.stock_quantity,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at
        )

class GetProductUseCase:
    """Use case for getting a product by ID"""
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
    
    def execute(self, product_id: int) -> ProductResponse:
        """Execute the get product use case"""
        try:
            product = self.product_service.get_product_by_id(product_id)
            return self._to_response(product)
        except ProductNotFoundException as e:
            raise e
    
    def _to_response(self, product) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name.value,
            description=product.description,
            price=product.price.value,
            category=product.category.value,
            stock_quantity=product.stock_quantity,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at
        )

class GetProductsUseCase:
    """Use case for getting all products"""
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
    
    def execute(self, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        """Execute the get products use case"""
        products = self.product_service.get_all_products(skip=skip, limit=limit)
        return [self._to_response(product) for product in products]
    
    def _to_response(self, product) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name.value,
            description=product.description,
            price=product.price.value,
            category=product.category.value,
            stock_quantity=product.stock_quantity,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at
        )

class GetProductsByCategoryUseCase:
    """Use case for getting products by category"""
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
    
    def execute(self, category: str, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        """Execute the get products by category use case"""
        products = self.product_service.get_products_by_category(category, skip=skip, limit=limit)
        return [self._to_response(product) for product in products]
    
    def _to_response(self, product) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name.value,
            description=product.description,
            price=product.price.value,
            category=product.category.value,
            stock_quantity=product.stock_quantity,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at
        )

class GetActiveProductsUseCase:
    """Use case for getting active products"""
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
    
    def execute(self, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        """Execute the get active products use case"""
        products = self.product_service.get_active_products(skip=skip, limit=limit)
        return [self._to_response(product) for product in products]
    
    def _to_response(self, product) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name.value,
            description=product.description,
            price=product.price.value,
            category=product.category.value,
            stock_quantity=product.stock_quantity,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at
        )

class UpdateProductUseCase:
    """Use case for updating a product"""
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
    
    def execute(self, product_id: int, request: UpdateProductRequest) -> ProductResponse:
        """Execute the update product use case"""
        try:
            product = self.product_service.update_product(
                product_id=product_id,
                name=request.name,
                description=request.description,
                category=request.category,
                price=request.price,
                stock_quantity=request.stock_quantity,
                is_active=request.is_active
            )
            return self._to_response(product)
        except ProductNotFoundException as e:
            raise e
    
    def _to_response(self, product) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name.value,
            description=product.description,
            price=product.price.value,
            category=product.category.value,
            stock_quantity=product.stock_quantity,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at
        )

class DeleteProductUseCase:
    """Use case for deleting a product"""
    
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
    
    def execute(self, product_id: int) -> bool:
        """Execute the delete product use case"""
        try:
            return self.product_service.delete_product(product_id)
        except ProductNotFoundException as e:
            raise e 