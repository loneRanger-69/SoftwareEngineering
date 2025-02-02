import pytest

import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_dough_create_read_delete(db):  # NOSONAR
    new_dough_name = 'test'
    new_dough_price = 3.0
    new_dough_description = 'description'
    new_dough_stock = 30
    number_of_doughs_before = len(dough_crud.get_all_doughs(db))

    # Arrange: Instantiate a new user object
    dough = DoughCreateSchema(name=new_dough_name, price=new_dough_price, description=new_dough_description,
                              stock=new_dough_stock)

    # Act: Add user to database
    db_dough = dough_crud.create_dough(dough, db)
    created_dough_id = db_dough.id

    # Assert: One more user in database
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before + 1

    # Act: Re-read user from database
    read_dough = dough_crud.get_dough_by_id(created_dough_id, db)

    # Assert: Correct user was stored in database
    assert read_dough.id == created_dough_id
    assert read_dough.name == new_dough_name

    # Act: Delete user
    dough_crud.delete_dough_by_id(created_dough_id, db)

    # Assert: Correct number of users in database after deletion
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before

    # Assert: Correct user was deleted from database
    deleted_dough = dough_crud.get_dough_by_id(created_dough_id, db)
    assert deleted_dough is None
