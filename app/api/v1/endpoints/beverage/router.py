import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import app.api.v1.endpoints.beverage.crud as beverage_crud
from app.api.v1.endpoints.beverage.schemas import BeverageSchema, BeverageCreateSchema, BeverageListItemSchema
from app.database.connection import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get('', response_model=List[BeverageListItemSchema], tags=['beverage'])
def get_all_beverages(db: Session = Depends(get_db)):
    logging.info('GET request to retrieve all beverages')
    beverages = beverage_crud.get_all_beverages(db)
    return beverages


@router.post('', response_model=BeverageSchema, status_code=status.HTTP_201_CREATED, tags=['beverage'])
def create_beverage(beverage: BeverageCreateSchema,
                    request: Request,
                    db: Session = Depends(get_db)):
    beverage_found = beverage_crud.get_beverage_by_name(beverage.name, db)

    if beverage_found:
        url = request.url_for('get_beverage', beverage_id=beverage_found.id)
        logging.info('Beverage with name {} already exists, redirecting to GET endpoint'.format(beverage.name))
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    new_beverage = beverage_crud.create_beverage(beverage, db)
    return new_beverage


@router.put('/{beverage_id}', response_model=BeverageSchema, tags=['beverage'])
def update_beverage(
        beverage_id: uuid.UUID,
        changed_beverage: BeverageCreateSchema,
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
):
    beverage_found = beverage_crud.get_beverage_by_id(beverage_id, db)

    if beverage_found:
        if beverage_found.name == changed_beverage.name:
            beverage_crud.update_beverage(beverage_found, changed_beverage, db)
            logging.info('Beverage with id {} updated successfully'.format(beverage_id))
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            beverage_name_found = beverage_crud.get_beverage_by_name(changed_beverage.name, db)
            if beverage_name_found:
                url = request.url_for('get_beverage', beverage_id=beverage_name_found.id)
                logging.info('Beverage with name {} '
                             'already exists, redirecting to GET endpoint'.format(changed_beverage.name))
                return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
            else:
                updated_beverage = beverage_crud.create_beverage(changed_beverage, db)
                response.status_code = status.HTTP_201_CREATED
                logging.info('Beverage with id {} not found, creating new beverage'.format(beverage_id))
    else:
        logging.warning('Beverage with id {} not found'.format(beverage_id))
        raise HTTPException(status_code=404)

    return updated_beverage


@router.get('/{beverage_id}', response_model=BeverageSchema, tags=['beverage'])
def get_beverage(
        beverage_id: uuid.UUID,
        db: Session = Depends(get_db),
):
    beverage = beverage_crud.get_beverage_by_id(beverage_id, db)

    if not beverage:
        logging.warning('Beverage with id {} not found'.format(beverage_id))
        raise HTTPException(status_code=404, detail='Item not found')

    return beverage


@router.delete('/{beverage_id}', response_model=None, tags=['beverage'])
def delete_beverage(
        beverage_id: uuid.UUID,
        db: Session = Depends(get_db)):
    beverage = beverage_crud.get_beverage_by_id(beverage_id, db)

    if not beverage:
        logging.warning('Attempted to delete beverage with id {} but beverage not found'.format(beverage_id))
        raise HTTPException(status_code=404, detail='Item not found')

    beverage_crud.delete_beverage_by_id(beverage_id, db)
    logging.info('Beverage with id {} deleted successfully'.format(beverage_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
