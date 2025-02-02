import pytest

import app.api.v1.endpoints.order.crud as order_crud
from app.api.v1.endpoints.order.schemas import OrderCreateSchema
from app.database.connection import SessionLocal

import app.api.v1.endpoints.order.address.crud as address_crud
from app.api.v1.endpoints.order.address.schemas import AddressCreateSchema

import app.api.v1.endpoints.user.crud as user_crud
from app.api.v1.endpoints.user.schemas import UserCreateSchema

import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema

import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_order_create_read_delete(db):
    # Arrange
    new_address_schema = AddressCreateSchema(
        street='Test',
        post_code='Test',
        house_number=1,
        country='Test',
        town='Test',
        first_name='Test',
        last_name='Test',
    )
    new_address = address_crud.create_address(new_address_schema, db)

    new_user_schema = UserCreateSchema(username='Test')
    new_user = user_crud.create_user(new_user_schema, db)

    # Define the order schema using the newly created address
    new_order_schema = OrderCreateSchema(
        user_id=new_user.id,
        address=new_address_schema,
    )
    new_dough_create_schema = DoughCreateSchema(
        name='test2',
        price=1.5,
        description='description',
        stock=3,
    )
    new_dough_id = dough_crud.create_dough(new_dough_create_schema, db).id

    pizza_type_schema = PizzaTypeCreateSchema(
        name='test1',
        price=1.5,
        description='description',
        dough_id=new_dough_id,
    )
    new_pizza_type = pizza_type_crud.create_pizza_type(pizza_type_schema, db)

    number_of_orders_before = len(order_crud.get_all_orders(db))

    # Act: Add order to database
    new_order = order_crud.create_order(new_order_schema, db)
    created_order_id = new_order.id

    number_of_orders_preparing = len(order_crud.get_orders_by_status(order_crud.OrderStatus.PREPARING, db))

    # Assert: One more order in database
    orders = order_crud.get_all_orders(db)
    assert len(orders) == number_of_orders_before + 1

    # Act: Re-read order from database
    read_order = order_crud.get_order_by_id(created_order_id, db)

    # Assert: Correct order was stored in database
    assert read_order.id == created_order_id
    assert read_order.user_id == new_user.id
    assert read_order.address_id == new_order.address_id  # Ensure address ID matches

    # Act: Update order status
    order_crud.update_order_status(read_order, order_crud.OrderStatus.PREPARING, db)

    # Assert: Correct status was stored in database
    read_order = order_crud.get_order_by_id(created_order_id, db)
    assert read_order.order_status == order_crud.OrderStatus.PREPARING

    # Act: Add Pizza to order
    all_pizzas_before = order_crud.get_all_pizzas_of_order(new_order, db)
    order_crud.add_pizza_to_order(new_order, new_pizza_type, db)

    # Assert: Pizza added to order
    all_pizzas = order_crud.get_all_pizzas_of_order(new_order, db)
    assert order_crud.get_pizza_by_id(all_pizzas[0].id, db)
    assert len(all_pizzas_before) + 1 == len(all_pizzas)

    # Act: Delete order
    order_crud.delete_order_by_id(created_order_id, db)

    # Assert: Correct number of orders in database after deletion
    orders = order_crud.get_all_orders(db)
    assert len(orders) == number_of_orders_before
    orders = order_crud.get_orders_by_status(order_crud.OrderStatus.PREPARING, db)
    assert len(orders) == number_of_orders_preparing

    # Assert: Correct order was deleted from database
    deleted_order = order_crud.get_order_by_id(created_order_id, db)
    assert deleted_order is None

    address_crud.delete_address_by_id(new_address.id, db)
    user_crud.delete_user_by_id(new_user.id, db)
    pizza_type_crud.delete_pizza_type_by_id(new_pizza_type.id, db)
    dough_crud.delete_dough_by_id(new_dough_id, db)
