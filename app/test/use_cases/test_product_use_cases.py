from app.schemas.category import Category
from app.schemas.product import Product
from app.db.models import Product as ProductModel, Category as CategoryModel
from app.use_cases.product_use_cases import ProductUseCases


def test_add_product_uc(db_session):
    uc = ProductUseCases(db_session)

    product = Product(
        name='Camisa Mike',
        slug='camisa-mike',
        price=22.99,
        stock=50,

    )

    uc.add_product(product=product, category_slug="roupa")
    products_on_db = db_session.query(ProductModel).first()

    assert products_on_db.name == product.name
    assert products_on_db.slug == product.slug
    assert products_on_db.price == product.price
    assert products_on_db.stock == product.stock
    assert products_on_db.category.slug == "roupa"

    db_session.delete(products_on_db)
    db_session.commit()

