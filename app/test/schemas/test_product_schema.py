import pytest

from app.schemas.product import Product, ProductOutput
from app.schemas.category import CategoryOutput


def test_product_schema():
    product = Product(
        name='Camisa Mike',
        slug='camisa-mike',
        price=22.99,
        stock=50
    )

    assert product.dict() == {
        'name': 'Camisa Mike',
        'slug': 'camisa-mike',
        'price': 22.99,
        'stock': 50
    }


def test_product_schema_invalid_slug():
    with pytest.raises(ValueError):
        product = Product(
            name='Camisa Mike',
            slug='camisa mike',
            price=22.99,
            stock=50
        )

    with pytest.raises(ValueError):
        product = Product(
            name='Camisa Mike',
            slug='cão',
            price=22.99,
            stock=50
        )

    with pytest.raises(ValueError):
        product = Product(
            name='Camisa Mike',
            slug='Camisa-Mike',
            price=22.99,
            stock=50
        )


def test_product_schema_invalid_price():
    with pytest.raises(ValueError):
        product = Product(
            name='Camisa Mike',
            slug='camisa-mike',
            price=0,
            stock=50
        )


def test_product_output_schema():
    category = CategoryOutput(id=1, name='Roupa', slug='roupa')

    product_output = ProductOutput(
        id=1,
        name='Camisa',
        slug='camisa',
        price=10,
        stock=10,
        category=category
    )

    print(product_output.dict())

    assert product_output.dict() == {
        'id': 1,
        'name': 'Camisa',
        'slug': 'camisa',
        'price': 10,
        'stock': 10,
        'category': category
    }
