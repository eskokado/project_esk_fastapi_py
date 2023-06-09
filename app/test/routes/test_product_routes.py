from fastapi.testclient import TestClient
from fastapi import status
from fastapi_pagination import Page

from app.db.models import Product as ProductModel
from app.main import app
from app.schemas.product import ProductOutput
from app.use_cases.product_use_cases import ProductUseCases
from app.db.models import Product

client = TestClient(app)
headers = {'Authorization': 'Bearer token'}
client.headers = headers


def test_add_product_route(db_session, categories_on_db):
    body = {
        "category_slug": categories_on_db[0].slug,
        "product": {
            "name": "Camisa Mike",
            "slug": "camisa-mike",
            "price": 23.99,
            "stock": 23
        }
    }

    response = client.post('/products/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 1

    db_session.delete(products_on_db[0])
    db_session.commit()


def test_add_product_invalid_category_slug(db_session):
    body = {
        "category_slug": "invalid",
        "product": {
            "name": "Camisa Mike",
            "slug": "camisa-mike",
            "price": 23.99,
            "stock": 23
        }
    }

    response = client.post('/products/add', json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 0


def test_update_product_route(db_session, product_on_db):
    body = {
        "name": "Updated camisa",
        "slug": "updated-camisa",
        "price": 23.99,
        "stock": 100
    }

    response = client.put(f'/products/update/{product_on_db.id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    db_session.refresh(product_on_db)

    assert product_on_db.name == "Updated camisa"
    assert product_on_db.slug == "updated-camisa"
    assert product_on_db.price == 23.99
    assert product_on_db.stock == 100


def test_update_product_route_invalid_id(db_session):
    body = {
        "name": "Updated camisa",
        "slug": "updated-camisa",
        "price": 23.99,
        "stock": 100
    }

    response = client.put(f'/products/update/99999', json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product_route(db_session, product_on_db):
    response = client.delete(f'/products/delete/{product_on_db.id}')

    assert response.status_code == status.HTTP_204_NO_CONTENT

    product_on_db = db_session.query(ProductModel).all()

    assert len(product_on_db) == 0


def test_delete_product_route_invalid_id(db_session, product_on_db):
    response = client.delete(f'/products/delete/{99999999999}')

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_products_route(db_session, products_on_db):
    response = client.get('/products/list?page=1&size=2')

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # assert 'items' in data
    # assert len(data['items']) == 2

    # page = Page[ProductOutput].parse_obj(data)
    #
    # assert page.items[0].name == products_on_db[0].name
    # assert page.items[0].category.name == products_on_db[0].category.name
    # assert page.total == len(products_on_db)
    # assert page.page == 1
    # assert page.size == 2
    # assert page.pages == len(products_on_db)


# assert 'items' in data
# assert len(data['items']) == 2
# assert data['items'][0] == {
#     "id": products_on_db[0].id,
#     "name": products_on_db[0].name,
#     "slug": products_on_db[0].slug,
#     "price": products_on_db[0].price,
#     "stock": products_on_db[0].stock,
#     "category": {
#         "name": products_on_db[0].category.name,
#         "slug": products_on_db[0].category.slug
#     }
# }
#

def test_list_products_with_search_route(db_session, products_on_db):
    response = client.get(f'/products/list?search=carro')

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # assert 'items' in data
    # assert len(data['items']) == 1
