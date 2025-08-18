from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..schemas import ProductCreateRequest, ProductUpdateRequest, ProductResponse
from ....application.products.use_cases import (
    CreateProductUseCase,
    GetProductUseCase,
    GetProductsUseCase,
    GetProductsByCategoryUseCase,
    GetActiveProductsUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase
)
from ....application.products.dto import CreateProductRequest as CreateProductDTO, UpdateProductRequest as UpdateProductDTO
from ....infrastructure.database.connection import get_db
from ....infrastructure.repositories.product_repository import SQLAlchemyProductRepository
from ....domains.products.services import ProductService

router = APIRouter()

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Dependency to get product service with repository"""
    product_repository = SQLAlchemyProductRepository(db)
    return ProductService(product_repository)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_request: ProductCreateRequest,
    product_service: ProductService = Depends(get_product_service)
):
    """Create a new product"""
    try:
        use_case = CreateProductUseCase(product_service)
        dto = CreateProductDTO(
            name=product_request.name,
            category=product_request.category,
            price=product_request.price,
            description=product_request.description,
            stock_quantity=product_request.stock_quantity
        )
        result = use_case.execute(dto)
        return ProductResponse(**result.__dict__)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    product_service: ProductService = Depends(get_product_service)
):
    """Get all products with optional category filtering"""
    if category:
        use_case = GetProductsByCategoryUseCase(product_service)
        results = use_case.execute(category=category, skip=skip, limit=limit)
    else:
        use_case = GetProductsUseCase(product_service)
        results = use_case.execute(skip=skip, limit=limit)
    return [ProductResponse(**result.__dict__) for result in results]

@router.get("/active", response_model=List[ProductResponse])
def get_active_products(
    skip: int = 0,
    limit: int = 100,
    product_service: ProductService = Depends(get_product_service)
):
    """Get only active products"""
    use_case = GetActiveProductsUseCase(product_service)
    results = use_case.execute(skip=skip, limit=limit)
    return [ProductResponse(**result.__dict__) for result in results]

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
):
    """Get a specific product by ID"""
    try:
        use_case = GetProductUseCase(product_service)
        result = use_case.execute(product_id)
        return ProductResponse(**result.__dict__)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_request: ProductUpdateRequest,
    product_service: ProductService = Depends(get_product_service)
):
    """Update a product"""
    try:
        use_case = UpdateProductUseCase(product_service)
        dto = UpdateProductDTO(
            name=product_request.name,
            description=product_request.description,
            category=product_request.category,
            price=product_request.price,
            stock_quantity=product_request.stock_quantity,
            is_active=product_request.is_active
        )
        result = use_case.execute(product_id, dto)
        return ProductResponse(**result.__dict__)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
):
    """Delete a product"""
    try:
        use_case = DeleteProductUseCase(product_service)
        use_case.execute(product_id)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) 