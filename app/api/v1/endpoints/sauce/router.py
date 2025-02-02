import uuid
from typing import List
import logging

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import app.api.v1.endpoints.sauce.crud as sauce_crud
from app.api.v1.endpoints.sauce.schemas import SauceSchema, SauceCreateSchema, SauceListItemSchema, SauceSpiciness
from app.database.connection import SessionLocal

router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('', response_model=List[SauceListItemSchema], tags=['sauce'])
def get_all_sauces(db: Session = Depends(get_db)):
    sauces = sauce_crud.get_all_sauces(db)
    return sauces


@router.get('/{sauce_id}', response_model=SauceSchema, tags=['sauce'])
def get_sauce(sauce_id: uuid.UUID, db: Session = Depends(get_db)):
    sauce = sauce_crud.get_sauce_by_id(sauce_id, db)
    if not sauce:
        raise HTTPException(status_code=404)
    return sauce


@router.post('', response_model=SauceSchema, status_code=status.HTTP_201_CREATED, tags=['sauce'])
def create_sauce(sauce: SauceCreateSchema, request: Request, db: Session = Depends(get_db)):
    sauce_found = sauce_crud.get_sauce_by_name(sauce.name, db)
    if sauce_found:
        url = request.url_for('get_sauce', sauce_id=sauce_found.id)
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    new_sauce = sauce_crud.create_sauce(sauce, db)
    return new_sauce


@router.put('/{sauce_id}', response_model=SauceSchema, tags=['sauce'])
def update_sauce(sauce_id: uuid.UUID,
                 changed_sauce: SauceCreateSchema,
                 request: Request,
                 response: Response,
                 db: Session = Depends(get_db)):
    sauce_found = sauce_crud.get_sauce_by_id(sauce_id, db)

    if sauce_found:
        if sauce_found.name == changed_sauce.name:
            sauce_crud.update_sauce(sauce_found, changed_sauce, db)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            sauce_name_found = sauce_crud.get_sauce_by_name(changed_sauce.name, db)
            if sauce_name_found:
                url = request.url_for('get_sauce', topping_id=sauce_name_found.id)
                return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
            else:
                updated_sauce = sauce_crud.create_sauce(changed_sauce, db)
                response.status_code = status.HTTP_201_CREATED
    else:
        raise HTTPException(status_code=404)

    return updated_sauce


@router.delete('/{sauce_id}', response_class=Response, tags=['sauce'])
def delete_sauce(sauce_id: uuid.UUID, db: Session = Depends(get_db)):
    sauce = sauce_crud.get_sauce_by_id(sauce_id, db)
    if not sauce:
        raise HTTPException(status_code=404, detail='Item not found')

    sauce_crud.delete_sauce_by_id(sauce_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/spiciness/{spiciness}', response_model=List[SauceListItemSchema], tags=['sauce'])
def get_sauces_by_spiciness(spiciness: SauceSpiciness, db: Session = Depends(get_db)):
    sauces = sauce_crud.get_sauces_by_spiciness_level(spiciness, db)
    if not sauces:
        raise HTTPException(status_code=404, detail='No sauces found with the specified Scoville level')
    return sauces
