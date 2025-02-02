import logging
import uuid
from sqlalchemy.orm import Session
from app.api.v1.endpoints.pizza_type.schemas import \
    PizzaTypeCreateSchema, \
    PizzaTypeToppingQuantityCreateSchema, \
    PizzaTypeSauceQuantityCreateSchema
from app.database.models import PizzaType, PizzaTypeToppingQuantity, PizzaTypeSauceQuantity


def create_pizza_type(schema: PizzaTypeCreateSchema, db: Session):
    entity = PizzaType(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('Pizza type created with name {}'.format(entity.name))
    return entity


def get_pizza_type_by_id(pizza_type_id: uuid.UUID, db: Session):
    entity = db.query(PizzaType).filter(PizzaType.id == pizza_type_id).first()
    logging.info('Pizza type retrieved with id {}'.format(pizza_type_id))
    return entity


def get_pizza_type_by_name(pizza_type_name: str, db: Session):
    entity = db.query(PizzaType).filter(PizzaType.name == pizza_type_name).first()
    logging.info('Pizza type retrieved with name {}'.format(pizza_type_name))
    return entity


def get_all_pizza_types(db: Session):
    entities = db.query(PizzaType).all()
    logging.info('Retrieved all pizza types, count: {}'.format(len(entities)))
    return entities


def update_pizza_type(pizza_type: PizzaType, changed_pizza_type: PizzaTypeCreateSchema, db: Session):
    for key, value in changed_pizza_type.dict().items():
        setattr(pizza_type, key, value)
    db.commit()
    db.refresh(pizza_type)
    logging.info('Pizza type updated with id {}'.format(pizza_type.id))
    return pizza_type


def delete_pizza_type_by_id(pizza_type_id: uuid.UUID, db: Session):
    entity = get_pizza_type_by_id(pizza_type_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Pizza type deleted with id {}'.format(pizza_type_id))
    else:
        logging.warning('Attempted to delete pizza type with id {} but pizza type not found'.format(pizza_type_id))


def create_topping_quantity(pizza_type: PizzaType, schema: PizzaTypeToppingQuantityCreateSchema, db: Session):
    entity = PizzaTypeToppingQuantity(**schema.dict())
    pizza_type.toppings.append(entity)
    db.commit()
    db.refresh(pizza_type)
    logging.info('Topping quantity created for pizza type with id {}'.format(pizza_type.id))
    return entity


def get_topping_quantity_by_id(pizza_type_id: uuid.UUID, topping_id: uuid.UUID, db: Session):
    entity = db.query(PizzaTypeToppingQuantity) \
        .filter(PizzaTypeToppingQuantity.topping_id == topping_id,
                PizzaTypeToppingQuantity.pizza_type_id == pizza_type_id) \
        .first()
    logging.info('Topping quantity retrieved for pizza type id {}'
                 ' and topping id {}'.format(pizza_type_id, topping_id))
    return entity


def get_joined_topping_quantities_by_pizza_type(pizza_type_id: uuid.UUID, db: Session):
    entities = db.query(PizzaTypeToppingQuantity) \
        .filter(PizzaTypeToppingQuantity.pizza_type_id == pizza_type_id)
    logging.info('Retrieved all topping quantities for pizza type id {},'
                 ' count: {}'.format(pizza_type_id, entities.count()))
    return entities.all()


def create_sauce_quantity(
        pizza_type: PizzaType,
        schema: PizzaTypeSauceQuantityCreateSchema,
        db: Session,
):
    entity = PizzaTypeSauceQuantity(**schema.dict())
    pizza_type.sauces.append(entity)
    db.commit()
    logging.info(f'Created new sauce quantity with ID: {entity.sauce_id} for pizza type {pizza_type.name}')
    db.refresh(pizza_type)
    return entity


def get_sauce_quantity_by_id(
        pizza_type_id: uuid.UUID,
        sauce_id: uuid.UUID,
        db: Session,
):
    logging.info(f' Looking for Sauce Quantity by ID {pizza_type_id}')
    entity = db.query(PizzaTypeSauceQuantity) \
        .filter(PizzaTypeSauceQuantity.sauce_id == sauce_id,
                PizzaTypeSauceQuantity.pizza_type_id == pizza_type_id) \
        .first()
    return entity


def get_joined_sauce_quantities_by_pizza_type(
        pizza_type_id: uuid.UUID,
        db: Session,
):
    logging.info(f' Looking for Joined Sauce Quantity by ID {pizza_type_id}')
    entities = db.query(PizzaTypeSauceQuantity) \
        .filter(PizzaTypeSauceQuantity.pizza_type_id == pizza_type_id)
    return entities.all()
