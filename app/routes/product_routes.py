from typing import List
from fastapi import APIRouter, Response, Depends, status, Query
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session, auth
from app.use_cases.product_use_cases import ProductUseCases
from app.schemas.product import Product, ProductInput, ProductOutput

router = APIRouter(prefix="/products", tags=["Product"], dependencies=[Depends(auth)])


@router.post("/add", status_code=status.HTTP_201_CREATED, description="Add new product")
def add_product(
    product_input: ProductInput,
    db_session: Session = Depends(get_db_session)
):
    uc = ProductUseCases(db_session=db_session)
    uc.add_product(
        product=product_input.product,
        category_slug=product_input.category_slug
    )

    return Response(status_code=status.HTTP_201_CREATED)


@router.put("/update/{id}", status_code=status.HTTP_200_OK, description="Update product by id")
def update_product(
        id: int,
        product: Product,
        db_session: Session = Depends(get_db_session)
):
    uc = ProductUseCases(db_session=db_session)
    uc.update_product(id=id, product=product)

    return Response(status_code=status.HTTP_200_OK)


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete product by id")
def delete_product(
        id: int,
        db_session: Session = Depends(get_db_session)
):
    uc = ProductUseCases(db_session=db_session)
    uc.delete_product(id=id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/list", response_model=Page[ProductOutput], status_code=status.HTTP_200_OK, description="List product")
def list_products(
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(50, ge=1, le=100, description="Page size"),
        search: str = '',
        db_session: Session = Depends(get_db_session)
):
    uc = ProductUseCases(db_session=db_session)
    response = uc.list_products(page=page, size=size, search=search)

    return response
