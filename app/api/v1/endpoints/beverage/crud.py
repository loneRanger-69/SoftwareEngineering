import logging
import uuid

from sqlalchemy.orm import Session

from app.api.v1.endpoints.beverage.schemas import BeverageCreateSchema
from app.database.models import Beverage


def create_beverage(schema: BeverageCreateSchema, db: Session):
    entity = Beverage(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('Beverage created with name {}'.format(entity.name))
    return entity


def get_beverage_by_id(beverage_id: uuid.UUID, db: Session):
    entity = db.query(Beverage).filter(Beverage.id == beverage_id).first()
    if entity:
        logging.info('Beverage retrieved with id {}'.format(beverage_id))
    else:
        logging.warning('Beverage with id {} not found'.format(beverage_id))
    return entity


def get_beverage_by_name(beverage_name: str, db: Session):
    entity = db.query(Beverage).filter(Beverage.name == beverage_name).first()
    return entity


def get_all_beverages(db: Session):
    beverages = db.query(Beverage).all()
    logging.info('Retrieved all beverages, count: {}'.format(len(beverages)))
    return db.query(Beverage).all()


def update_beverage(beverage: Beverage, changed_beverage: BeverageCreateSchema, db: Session):
    for key, value in changed_beverage.dict().items():
        setattr(beverage, key, value)

    db.commit()
    db.refresh(beverage)
    logging.info('Beverage updated with id {}'.format(beverage.id))
    return beverage


def delete_beverage_by_id(beverage_id: uuid.UUID, db: Session):
    entity = get_beverage_by_id(beverage_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Beverage deleted with id {}'.format(beverage_id))
