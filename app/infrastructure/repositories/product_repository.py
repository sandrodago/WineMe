from sqlalchemy.orm import Session
from typing import List, Optional
from ...domains.products.repository import ProductRepository
from ...domains.products.domain import Product, ProductCategory
from ..database.models import ProductModel

class SQLAlchemyProductRepository(ProductRepository):
    """SQLAlchemy implementation of ProductRepository"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create(self, product: Product) -> Product:
        """Create a new product"""
        db_product = ProductModel(
            name=product.name.value,
            description=product.description,
            price=product.price.value,
            category=product.category.value,
            stock_quantity=product.stock_quantity,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        
        # Convert back to domain entity
        return self._to_domain_entity(db_product)
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        db_product = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._to_domain_entity(db_product) if db_product else None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get all products with pagination"""
        db_products = self.db.query(ProductModel).offset(skip).limit(limit).all()
        return [self._to_domain_entity(db_product) for db_product in db_products]
    
    def get_by_category(self, category: ProductCategory, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get products by category"""
        db_products = self.db.query(ProductModel).filter(ProductModel.category == category.value).offset(skip).limit(limit).all()
        return [self._to_domain_entity(db_product) for db_product in db_products]
    
    def get_active_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get only active products"""
        db_products = self.db.query(ProductModel).filter(ProductModel.is_active == True).offset(skip).limit(limit).all()
        return [self._to_domain_entity(db_product) for db_product in db_products]
    
    def update(self, product: Product) -> Product:
        """Update product"""
        db_product = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()
        if db_product:
            # Update the SQLAlchemy model attributes
            db_product.name = product.name.value
            db_product.description = product.description
            db_product.price = product.price.value
            db_product.category = product.category.value
            db_product.stock_quantity = product.stock_quantity
            db_product.is_active = product.is_active
            db_product.updated_at = product.updated_at
            self.db.commit()
            self.db.refresh(db_product)
            return self._to_domain_entity(db_product)
        return product
    
    def delete(self, product_id: int) -> bool:
        """Delete product"""
        db_product = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
            return True
        return False
    
    def exists_by_name(self, name: str) -> bool:
        """Check if product exists by name"""
        return self.db.query(ProductModel).filter(ProductModel.name == name).first() is not None
    
    def _to_domain_entity(self, db_product: ProductModel) -> Product:
        """Convert SQLAlchemy model to domain entity"""
        from ...domains.products.domain import ProductName, ProductCategory, Price
        
        return Product(
            id=db_product.id,
            name=ProductName(db_product.name),
            description=db_product.description,
            price=Price(db_product.price),
            category=ProductCategory(db_product.category),
            stock_quantity=db_product.stock_quantity,
            is_active=db_product.is_active,
            created_at=db_product.created_at,
            updated_at=db_product.updated_at
        ) 