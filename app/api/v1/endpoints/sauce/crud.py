import logging
import uuid
from sqlalchemy.orm import Session
from app.database.models import Sauce
from app.api.v1.endpoints.sauce.schemas import SauceCreateSchema, SauceListItemSchema, SauceSpiciness

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_sauce(schema: SauceCreateSchema, db: Session):
    entity = Sauce(**schema.dict())
    db.add(entity)
    db.commit()
    db.refresh(entity)
    logger.info('Sauce created with name {}'.format(entity.name))
    return entity


def get_sauce_by_id(sauce_id: uuid.UUID, db: Session):
    logger.info('Fetching sauce by ID: {}'.format(sauce_id))
    entity = db.query(Sauce).filter(Sauce.id == sauce_id).first()
    if entity:
        logger.info('Sauce found: {}'.format(entity.name))
    else:
        logger.warning('Sauce with ID {} not found'.format(sauce_id))
    return entity


def get_sauce_by_name(sauce_name: str, db: Session):
    logger.info('Fetching sauce by name: {}'.format(sauce_name))
    entity = db.query(Sauce).filter(Sauce.name == sauce_name).first()
    if entity:
        logger.info('Sauce found: {}'.format(entity.name))
    else:
        logger.warning('Sauce with name {} not found'.format(sauce_name))
    return entity


def get_all_sauces(db: Session):
    logger.info('Fetching all sauces')
    entities = db.query(Sauce).all()
    logger.info('Found {} sauces'.format(len(entities)))
    if entities:
        return_entities = []
        for entity in entities:
            list_item_entity = SauceListItemSchema(
                id=entity.id,
                name=entity.name,
                price=entity.price,
                description=entity.description,
                spiciness=entity.spiciness,
            )
            return_entities.append(list_item_entity)
        return return_entities
    return entities


def update_sauce(sauce: Sauce, changed_sauce: SauceCreateSchema, db: Session):
    logger.info('Updating sauce : {}'.format(sauce.name))
    for key, value in changed_sauce.dict().items():
        setattr(sauce, key, value)
    db.commit()
    db.refresh(sauce)
    logger.info('Sauce updated: {}'.format(sauce.name))
    return sauce


def delete_sauce_by_id(sauce_id: uuid.UUID, db: Session):
    logger.info('Deleting sauce with ID: {}'.format(sauce_id))
    entity = get_sauce_by_id(sauce_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logger.info('Sauce with ID {} deleted'.format(sauce_id))
        return True
    else:
        logger.warning('Sauce with ID {} not found for deletion'.format(sauce_id))
        return False


def get_sauces_by_spiciness_level(sauce_spiciness: SauceSpiciness, db: Session):
    logger.info('Fetching sauces with Spiciness level: {}'.format(sauce_spiciness))
    entities = db.query(Sauce).filter(Sauce.spiciness == sauce_spiciness).all()
    if entities:
        logger.info('Found {} sauces with Spiciness level {}'.format(len(entities), sauce_spiciness))
        return entities
    logger.warning('No sauces found with Spiciness level {}'.format(sauce_spiciness))
    return []
