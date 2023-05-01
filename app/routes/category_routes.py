from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.schemas.category import Category
from app.routes.deps import get_db_session
from app.use_cases.category_use_cases import CategoryUseCases


router = APIRouter(prefix='/categories', tags=['Category'])


@router.post('/add')
def add_category(
    category: Category,
    db_session: Session = Depends(get_db_session)
):
    uc = CategoryUseCases(db_session=db_session)
    uc.add_category(category=category)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/list')
def list_categories(
    db_session: Session = Depends(get_db_session)
):
    uc = CategoryUseCases(db_session=db_session)
    response = uc.list_categories()

    return response
