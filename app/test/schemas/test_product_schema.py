import pytest

from app.schemas.product import Product


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
