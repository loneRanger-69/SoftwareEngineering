import uuid
import logging
from typing import List
from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.dough.schemas import DoughSchema, DoughCreateSchema, DoughListItemSchema
from app.database.connection import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('', response_model=List[DoughListItemSchema], tags=['dough'])
def get_all_doughs(db: Session = Depends(get_db)):
    logging.info('Received request to fetch all doughs')
    return dough_crud.get_all_doughs(db)


@router.post('', response_model=DoughSchema, status_code=status.HTTP_201_CREATED, tags=['dough'])
def create_dough(dough: DoughCreateSchema, request: Request, db: Session = Depends(get_db)):
    logging.info('Received request to create dough: {}'.format(dough))
    dough_found = dough_crud.get_dough_by_name(dough.name, db)
    if dough_found:
        url = request.url_for('get_dough', dough_id=dough_found.id)
        logging.warning('Dough with name {} already exists, redirecting to {}'.format(dough.name, url))
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    new_dough = dough_crud.create_dough(dough, db)
    logging.info('Dough created successfully with name {}'.format(new_dough.name))
    return new_dough


@router.put('/{dough_id}', response_model=DoughSchema, tags=['dough'])
def update_dough(
        dough_id: uuid.UUID,
        changed_dough: DoughCreateSchema,
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
):
    logging.info('Received request to update dough with ID {}: {}'.format(dough_id, changed_dough))
    dough_found = dough_crud.get_dough_by_id(dough_id, db)
    updated_dough = None

    if dough_found:
        if dough_found.name == changed_dough.name:
            dough_crud.update_dough(dough_found, changed_dough, db)
            logging.info('Dough with ID {} updated successfully'.format(dough_id))
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            dough_name_found = dough_crud.get_dough_by_name(changed_dough.name, db)
            if dough_name_found:
                url = request.url_for('get_dough', dough_id=dough_name_found.id)
                logging.warning('Dough with name {} already exists,'
                                ' redirecting to {}'.format(changed_dough.name, url))
                return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
            else:
                updated_dough = dough_crud.create_dough(changed_dough, db)
                response.status_code = status.HTTP_201_CREATED
                logging.info('Dough created with new name {}'
                             ' and ID {}'.format(changed_dough.name, updated_dough.id))
    else:
        logging.error('Dough with ID {} not found'.format(dough_id))
        raise HTTPException(status_code=404)

    return updated_dough


@router.get('/{dough_id}', response_model=DoughSchema, tags=['dough'])
def get_dough(dough_id: uuid.UUID, db: Session = Depends(get_db)):
    logging.info('Received request to fetch dough with ID {}'.format(dough_id))
    dough = dough_crud.get_dough_by_id(dough_id, db)

    if not dough:
        logging.error('Dough with ID {} not found'.format(dough_id))
        raise HTTPException(status_code=404)
    return dough


@router.delete('/{dough_id}', response_model=None, tags=['dough'])
def delete_dough(dough_id: uuid.UUID, db: Session = Depends(get_db)):
    logging.info('Received request to delete dough with ID {}'.format(dough_id))
    dough = dough_crud.get_dough_by_id(dough_id, db)

    if not dough:
        logging.error('Dough with ID {} not found'.format(dough_id))
        raise HTTPException(status_code=404, detail='Item not found')

    dough_crud.delete_dough_by_id(dough_id, db)
    logging.info('Dough with ID {} deleted successfully'.format(dough_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
