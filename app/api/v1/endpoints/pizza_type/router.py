import logging
import uuid
from typing import List, TypeVar
from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import app.api.v1.endpoints.dough.crud as dough_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
import app.api.v1.endpoints.sauce.crud as sauce_crud
import app.api.v1.endpoints.topping.crud as topping_crud
from app.api.v1.endpoints.dough.schemas import DoughSchema
from app.api.v1.endpoints.pizza_type.schemas import (JoinedPizzaTypeQuantitySchema, PizzaTypeSchema,
                                                     PizzaTypeCreateSchema, PizzaTypeToppingQuantityCreateSchema,
                                                     PizzaTypeSauceQuantityCreateSchema,
                                                     )
from app.database.connection import SessionLocal

WITH_ID_NOT_FOUND = 'Pizza type with id {} not found'

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('', response_model=List[PizzaTypeSchema], tags=['pizza_type'])
def get_all_pizza_types(db: Session = Depends(get_db)):
    logging.info('GET request to retrieve all pizza types')
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    return pizza_types


@router.post('', response_model=PizzaTypeSchema, tags=['pizza_type'])
def create_pizza_type(pizza_type: PizzaTypeCreateSchema, request: Request, response: Response,
                      db: Session = Depends(get_db)):
    logging.info('POST request to create a pizza type with payload: {}'.format(pizza_type))
    pizza_type_found = pizza_type_crud.get_pizza_type_by_name(pizza_type.name, db)
    if pizza_type_found:
        url = request.url_for('get_pizza_type', pizza_type_id=pizza_type_found.id)
        logging.info('Pizza type with name {} already exists, redirecting to GET endpoint'.format(pizza_type.name))
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    dough = dough_crud.get_dough_by_id(pizza_type.dough_id, db)
    if not dough:
        logging.error('Dough with id {} not found'.format(pizza_type.dough_id))
        raise HTTPException(status_code=404)
    new_pizza_type = pizza_type_crud.create_pizza_type(pizza_type, db)
    response.status_code = status.HTTP_201_CREATED
    return new_pizza_type


@router.put('/{pizza_type_id}', response_model=PizzaTypeSchema, tags=['pizza_type'])
def update_pizza_type(pizza_type_id: uuid.UUID, changed_pizza_type: PizzaTypeCreateSchema,
                      request: Request, response: Response, db: Session = Depends(get_db)):
    logging.info('PUT request to update pizza type id {}'
                 ' with payload: {}'.format(pizza_type_id, changed_pizza_type))
    pizza_type_found = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    updated_pizza_type = None
    if pizza_type_found:
        if pizza_type_found.name == changed_pizza_type.name:
            pizza_type_crud.update_pizza_type(pizza_type_found, changed_pizza_type, db)
            logging.info('Pizza type with id {} updated successfully'.format(pizza_type_id))
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            pizza_type_name_found = pizza_type_crud.get_pizza_type_by_name(changed_pizza_type.name, db)
            if pizza_type_name_found:
                url = request.url_for('get_pizza_type', pizza_type_id=pizza_type_name_found.id)
                logging.info('Pizza type with name {} already exists,'
                             ' redirecting to GET endpoint'.format(changed_pizza_type.name))
                return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
            else:
                updated_pizza_type = pizza_type_crud.create_pizza_type(changed_pizza_type, db)
                logging.info('Pizza type with id {} created successfully'.format(updated_pizza_type.id))
                response.status_code = status.HTTP_201_CREATED
    else:
        logging.error(WITH_ID_NOT_FOUND.format(pizza_type_id))
        raise HTTPException(status_code=404)
    return updated_pizza_type


@router.get('/{pizza_type_id}', response_model=PizzaTypeSchema, tags=['pizza_type'])
def get_pizza_type(pizza_type_id: uuid.UUID, db: Session = Depends(get_db)):
    logging.info('GET request to retrieve pizza type with id {}'.format(pizza_type_id))
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    if not pizza_type:
        logging.warning(WITH_ID_NOT_FOUND.format(pizza_type_id))
        raise HTTPException(status_code=404)
    return pizza_type


@router.delete('/{pizza_type_id}', response_model=None, tags=['pizza_type'])
def delete_pizza_type(pizza_type_id: uuid.UUID, db: Session = Depends(get_db)):
    logging.info('DELETE request to delete pizza type with id {}'.format(pizza_type_id))
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    if not pizza_type:
        logging.warning(WITH_ID_NOT_FOUND.format(pizza_type_id))
        raise HTTPException(status_code=404)
    pizza_type_crud.delete_pizza_type_by_id(pizza_type_id, db)
    logging.info('Pizza type with id {} deleted successfully'.format(pizza_type_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


MyPyEitherItem = TypeVar('MyPyEitherItem', List[PizzaTypeToppingQuantityCreateSchema],
                         List[JoinedPizzaTypeQuantitySchema], List[PizzaTypeSauceQuantityCreateSchema], None)


@router.get('/{pizza_type_id}/toppings', response_model=MyPyEitherItem, tags=['pizza_type'])
def get_pizza_type_toppings(pizza_type_id: uuid.UUID, response: Response, db: Session = Depends(get_db),
                            join: bool = False):
    logging.info('GET request to retrieve toppings for pizza type id {}'.format(pizza_type_id))
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    if not pizza_type:
        logging.warning(WITH_ID_NOT_FOUND.format(pizza_type_id))
        raise HTTPException(status_code=404)
    toppings = pizza_type.toppings
    if join:
        toppings = pizza_type_crud.get_joined_topping_quantities_by_pizza_type(pizza_type.id, db)
    return toppings


@router.post('/{pizza_type_id}/toppings', response_model=PizzaTypeToppingQuantityCreateSchema,
             status_code=status.HTTP_201_CREATED, tags=['pizza_type'])
def create_pizza_type_topping(pizza_type_id: uuid.UUID, topping_quantity: PizzaTypeToppingQuantityCreateSchema,
                              request: Request, response: Response, db: Session = Depends(get_db)):
    logging.info('POST request to create topping quantity for pizza type id {}'
                 ' with payload: {}'.format(pizza_type_id, topping_quantity))
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    if not pizza_type:
        logging.warning(WITH_ID_NOT_FOUND.format(pizza_type_id))
        raise HTTPException(status_code=404)
    if not topping_crud.get_topping_by_id(topping_quantity.topping_id, db):
        logging.warning(WITH_ID_NOT_FOUND.format(topping_quantity.topping_id))
        raise HTTPException(status_code=404)
    topping_quantity_found = pizza_type_crud.get_topping_quantity_by_id(pizza_type_id, topping_quantity.topping_id, db)
    if topping_quantity_found:
        url = request.url_for('get_pizza_type_toppings', pizza_type_id=topping_quantity_found.pizza_type_id)
        logging.info('Topping quantity already exists for pizza type id {},'
                     ' redirecting to GET endpoint'.format(pizza_type_id))
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    new_topping_quantity = pizza_type_crud.create_topping_quantity(pizza_type, topping_quantity, db)
    return new_topping_quantity


@router.get('/{pizza_type_id}/dough', response_model=DoughSchema, tags=['pizza_type'])
def get_pizza_type_dough(pizza_type_id: uuid.UUID, response: Response, db: Session = Depends(get_db)):
    logging.info('GET request to retrieve dough for pizza type id {}'.format(pizza_type_id))
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    if not pizza_type:
        logging.warning(WITH_ID_NOT_FOUND.format(pizza_type_id))
        raise HTTPException(status_code=404)
    dough = pizza_type.dough
    return dough


@router.get(
    '/{pizza_type_id}/sauces',
    response_model=MyPyEitherItem,
    tags=['pizza_type'],
)
def get_pizza_type_sauces(
        pizza_type_id: uuid.UUID,
        response: Response,
        db: Session = Depends(get_db),
        join: bool = False,
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)

    if not pizza_type:
        logging.error(f'Pizza type with ID {pizza_type_id} does not exist')
        raise HTTPException(status_code=404)

    sauces = pizza_type.sauces
    if join:
        sauces = pizza_type_crud.get_joined_sauce_quantities_by_pizza_type(pizza_type.id, db)
        logging.info(f'Retrieved {len(sauces)} sauces' f' from pizza type {pizza_type.name}')   # NOSONAR
    return sauces


@router.post(
    '/{pizza_type_id}/sauces',
    response_model=PizzaTypeSauceQuantityCreateSchema,
    status_code=status.HTTP_201_CREATED,
    tags=['pizza_type'],
)
def create_pizza_type_sauce(
        pizza_type_id: uuid.UUID,
        sauce_quantity: PizzaTypeSauceQuantityCreateSchema,
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    if not pizza_type:
        logging.error(f'Pizza type with ID {pizza_type_id} does not exist')
        raise HTTPException(status_code=404)

    if not sauce_crud.get_sauce_by_id(sauce_quantity.sauce_id, db):
        logging.error(f'Sauce with ID {sauce_quantity.sauce_id} does not exist')
        raise HTTPException(status_code=404)

    sauce_quantity_found = pizza_type_crud.get_sauce_quantity_by_id(pizza_type_id, sauce_quantity.sauce_id, db)
    if sauce_quantity_found:
        url = request.url_for('get_pizza_type_sauces', pizza_type_id=sauce_quantity_found.pizza_type_id)
        logging.warning(f'Sauce quantity for topping ID {sauce_quantity.sauce_id}'
                        f'on pizza type ID {pizza_type_id} already exists.')
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    new_sauce_quantity = pizza_type_crud.create_sauce_quantity(pizza_type, sauce_quantity, db)
    return new_sauce_quantity
