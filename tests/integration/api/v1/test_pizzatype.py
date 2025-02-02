import pytest

import app.api.v1.endpoints.dough.crud as dough_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_pizza_type_create_read_update_delete(db):
    # Arrange: Set up initial values
    dough_name = 'Test Dough'
    dough_price = 2.0
    dough_description = 'Test dough description'
    dough_stock = 100

    new_pizza_type_name = 'Test Pizza'
    new_pizza_type_price = 10.0
    new_pizza_type_description = 'Test pizza description'

    updated_pizza_type_name = 'Updated Test Pizza'
    updated_pizza_type_price = 12.0
    updated_pizza_type_description = 'Updated pizza description'

    # Create a dough first
    dough_schema = DoughCreateSchema(name=dough_name, price=dough_price, description=dough_description,
                                     stock=dough_stock)
    dough = dough_crud.create_dough(dough_schema, db)

    # Arrange: Instantiate a new pizza type object
    pizza_type_schema = PizzaTypeCreateSchema(name=new_pizza_type_name, price=new_pizza_type_price,
                                              description=new_pizza_type_description, dough_id=dough.id)

    # Act: Add pizza type to the database
    db_pizza_type = pizza_type_crud.create_pizza_type(pizza_type_schema, db)
    created_pizza_type_id = db_pizza_type.id

    # Assert: One more pizza type in database
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    assert any(pizza_type.id == created_pizza_type_id for pizza_type in pizza_types)

    # Act: Re-read pizza type from the database
    read_pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Correct pizza type was stored in the database
    assert read_pizza_type.id == created_pizza_type_id
    assert read_pizza_type.name == new_pizza_type_name

    # Arrange: Update the pizza type
    updated_pizza_type_schema = PizzaTypeCreateSchema(name=updated_pizza_type_name, price=updated_pizza_type_price,
                                                      description=updated_pizza_type_description, dough_id=dough.id)

    # Act: Update pizza type in the database
    pizza_type_crud.update_pizza_type(read_pizza_type, updated_pizza_type_schema, db)

    # Re-read the pizza type from the database
    updated_pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Correct pizza type was updated in the database
    assert updated_pizza_type.id == created_pizza_type_id
    assert updated_pizza_type.name == updated_pizza_type_name

    # Act: Delete pizza type
    pizza_type_crud.delete_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Pizza type was deleted from the database
    deleted_pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_type_id, db)
    assert deleted_pizza_type is None
