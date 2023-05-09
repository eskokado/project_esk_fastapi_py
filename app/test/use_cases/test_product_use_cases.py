import ipdb
import pytest

from app.schemas.product import Product, ProductOutput
from app.db.models import Product as ProductModel
from app.use_cases.product_use_cases import ProductUseCases
from fastapi.exceptions import HTTPException
from fastapi_pagination import Page


def test_add_product_uc(db_session, categories_on_db):
    uc = ProductUseCases(db_session)

    product = Product(
        name='Camisa Mike',
        slug='camisa-mike',
        price=22.99,
        stock=50,

    )

    uc.add_product(product=product, category_slug=categories_on_db[0].slug)
    products_on_db = db_session.query(ProductModel).first()

    assert products_on_db.name == product.name
    assert products_on_db.slug == product.slug
    assert products_on_db.price == product.price
    assert products_on_db.stock == product.stock
    assert products_on_db.category.slug == "roupa"

    db_session.delete(products_on_db)
    db_session.commit()


def test_add_product_data_invalid(db_session):
    uc = ProductUseCases(db_session)

    product = Product(
        name='Camisa Mike',
        slug='camisa-mike',
        price=22.99,
        stock=50,
    )

    with pytest.raises(HTTPException):
        uc.add_product(product=product, category_slug="qualquer-slug")


def test_update_product(db_session, product_on_db):
    product = Product(
        name='Camisa Mike',
        slug='camisa-mike',
        price=22.99,
        stock=50,
    )
    uc = ProductUseCases(db_session=db_session)
    uc.update_product(id=product_on_db.id, product=product)

    product_updated_on_db = db_session.query(ProductModel).filter_by(id=product_on_db.id).first()

    assert product_updated_on_db is not None
    assert product_updated_on_db.name == product.name
    assert product_updated_on_db.slug == product.slug
    assert product_updated_on_db.price == product.price
    assert product_updated_on_db.stock == product.stock


def test_update_product_invalid_id(db_session, product_on_db):
    product = Product(
        name='Camisa Mike',
        slug='camisa-mike',
        price=22.99,
        stock=50,
    )
    uc = ProductUseCases(db_session=db_session)
    with pytest.raises(HTTPException):
        uc.update_product(id=9999, product=product)


def test_delete_product(db_session, product_on_db):
    uc = ProductUseCases(db_session=db_session)
    uc.delete_product(id=product_on_db.id)

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 0


def test_delete_product_invalid_id(db_session):
    uc = ProductUseCases(db_session=db_session)
    with pytest.raises(HTTPException):
        uc.delete_product(id=9999)


def test_list_products(db_session, products_on_db):
    uc = ProductUseCases(db_session=db_session)
    page: Page = uc.list_products(page=1, size=2)

    assert 'items' in page.__dict__
    assert page.size == 2
    assert page.total == 2
    assert page.page == 1
    assert page.pages == 1

    assert page.items[0].name == products_on_db[0].name
    assert page.items[0].category.name == products_on_db[0].category.name


def test_list_products_with_search(db_session, products_on_db):
    uc = ProductUseCases(db_session=db_session)
    page = uc.list_products(search='carro')

    assert 'items' in page.__dict__
    assert page.size == 50
    assert page.total == 1
    assert page.page == 1
    assert page.pages == 1
