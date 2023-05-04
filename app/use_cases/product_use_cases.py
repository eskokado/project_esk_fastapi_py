from app.db.connection import Session
from app.schemas.product import Product, ProductOutput
from app.db.models import Product as ProductModel, Category as CategoryModel
from fastapi.exceptions import HTTPException
from fastapi import status


class ProductUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_product(self, product: Product, category_slug: str):
        category = self.db_session.query(CategoryModel).filter_by(slug=category_slug).first()
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No category was slug {category_slug}')
        product_model = ProductModel(**product.dict())
        product_model.category_id = category.id
        self.db_session.add(product_model)
        self.db_session.commit()

    def update_product(self, id: int, product: Product):
        product_on_db = self.db_session.query(ProductModel).filter_by(id=id).first()

        if product_on_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product was found - {product.name}")

        product_on_db.name = product.name
        product_on_db.slug = product.slug
        product_on_db.price = product.price
        product_on_db.stock = product.stock

        self.db_session.add(product_on_db)
        self.db_session.commit()

    def delete_product(self, id: int):
        product_on_db = self.db_session.query(ProductModel).filter_by(id=id).first()

        if product_on_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product was found - id {id}")

        self.db_session.delete(product_on_db)
        self.db_session.commit()

    def list_products(self):
        products_on_db = self.db_session.query(ProductModel).all()
        products_output = [
            self.serialize_product(product_model) for product_model in products_on_db
        ]
        return products_output

    def serialize_product(self, product_model: ProductModel):
        product_dict = product_model.__dict__
        product_dict['category'] = product_model.category.__dict__
        return ProductOutput(**product_dict)
