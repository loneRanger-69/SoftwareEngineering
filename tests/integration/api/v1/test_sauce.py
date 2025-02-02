import pytest

import app.api.v1.endpoints.sauce.crud as sauce_crud
from app.api.v1.endpoints.sauce.schemas import SauceCreateSchema, SauceSpiciness
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_sauce_create_read_delete(db):
    new_sauce_name = 'Test_sauce'
    number_of_sauces_before = len(sauce_crud.get_all_sauces(db))

    # Arrange: Instantiate a new sauce object
    sauce = SauceCreateSchema(name=new_sauce_name, price=1.99, description='A test sauce',
                              spiciness=SauceSpiciness.LEVEL1, stock=10)

    # Act: Add sauce to database
    db_sauce = sauce_crud.create_sauce(sauce, db)
    created_sauce_id = db_sauce.id

    # Assert: One more sauce in database
    sauces = sauce_crud.get_all_sauces(db)
    assert len(sauces) == number_of_sauces_before + 1

    # Act: Re-read sauce from database
    read_sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)

    # Assert: Correct sauce was stored in database
    assert read_sauce.id == created_sauce_id
    assert read_sauce.name == new_sauce_name

    # Act: Update price and scoville_level in database
    new_sauce_price = 4.99
    new_spiciness = SauceSpiciness.LEVEL2

    entities_before = sauce_crud.get_sauces_by_spiciness_level(new_spiciness, db)
    amount_entities_before = len(entities_before)

    update_sauce = SauceCreateSchema(name=new_sauce_name, price=new_sauce_price,
                                     description='A test sauce', spiciness=new_spiciness, stock=10)
    sauce_crud.update_sauce(read_sauce, update_sauce, db)

    # Act: Re-read sauce by name
    updated_sauce = sauce_crud.get_sauce_by_name(new_sauce_name, db)

    # Act : Get Sauce by Scoville_Level
    entities = sauce_crud.get_sauces_by_spiciness_level(new_spiciness, db)
    assert len(entities) == amount_entities_before + 1

    # Assert: New price in db
    assert new_sauce_price.__eq__(updated_sauce.price)

    # Act: Delete sauce
    sauce_crud.delete_sauce_by_id(created_sauce_id, db)

    # Assert: Correct number of sauce in database after deletion
    sauces = sauce_crud.get_all_sauces(db)
    assert len(sauces) == number_of_sauces_before

    # Assert: Correct sauce was deleted from database
    deleted_sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)
    assert deleted_sauce is None
