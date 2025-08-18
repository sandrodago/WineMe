from typing import List, Optional
from .domain import Product, ProductName, ProductCategory, Price, ProductNotFoundException
from .repository import ProductRepository

class ProductService:
    """Product domain service - contains business logic for product operations"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def create_product(self, name: str, category: str, price: float, description: Optional[str] = None, stock_quantity: int = 0) -> Product:
        """Create a new product with business rules"""
        # Create value objects
        product_name = ProductName(name)
        product_category = ProductCategory(category)
        product_price = Price(price)
        
        # Check business rules
        if self.product_repository.exists_by_name(name):
            raise ValueError(f"Product with name '{name}' already exists")
        
        # Create domain entity
        product = Product(
            name=product_name,
            category=product_category,
            price=product_price,
            description=description,
            stock_quantity=stock_quantity
        )
        
        # Save to repository
        return self.product_repository.create(product)
    
    def get_product_by_id(self, product_id: int) -> Product:
        """Get product by ID"""
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(f"Product with ID {product_id} not found")
        return product
    
    def get_all_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get all products with pagination"""
        return self.product_repository.get_all(skip=skip, limit=limit)
    
    def get_products_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get products by category"""
        product_category = ProductCategory(category)
        return self.product_repository.get_by_category(product_category, skip=skip, limit=limit)
    
    def get_active_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get only active products"""
        return self.product_repository.get_active_products(skip=skip, limit=limit)
    
    def update_product(self, product_id: int, name: Optional[str] = None, description: Optional[str] = None, 
                      category: Optional[str] = None, price: Optional[float] = None, 
                      stock_quantity: Optional[int] = None, is_active: Optional[bool] = None) -> Product:
        """Update product with business logic"""
        product = self.get_product_by_id(product_id)
        
        if name is not None:
            product.update_details(name=name)
        if description is not None:
            product.update_details(description=description)
        if category is not None:
            product.update_details(category=category)
        if price is not None:
            product.update_price(price)
        if stock_quantity is not None:
            product.update_stock(stock_quantity)
        if is_active is not None:
            if is_active:
                product.activate()
            else:
                product.deactivate()
        
        return self.product_repository.update(product)
    
    def delete_product(self, product_id: int) -> bool:
        """Delete product"""
        product = self.get_product_by_id(product_id)
        return self.product_repository.delete(product_id)
    
    def add_stock(self, product_id: int, quantity: int) -> Product:
        """Add stock to product"""
        product = self.get_product_by_id(product_id)
        product.add_stock(quantity)
        return self.product_repository.update(product)
    
    def remove_stock(self, product_id: int, quantity: int) -> Product:
        """Remove stock from product"""
        product = self.get_product_by_id(product_id)
        product.remove_stock(quantity)
        return self.product_repository.update(product)
    
    def activate_product(self, product_id: int) -> Product:
        """Activate product"""
        product = self.get_product_by_id(product_id)
        product.activate()
        return self.product_repository.update(product)
    
    def deactivate_product(self, product_id: int) -> Product:
        """Deactivate product"""
        product = self.get_product_by_id(product_id)
        product.deactivate()
        return self.product_repository.update(product) 