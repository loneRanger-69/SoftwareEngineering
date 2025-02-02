from sqlalchemy.orm import Session

from app.database.models import PizzaType


def ingredients_are_available(pizza_type: PizzaType):
    if pizza_type.dough.stock == 0:
        return False

    for topping_quantity in pizza_type.toppings:
        if topping_quantity.topping.stock < topping_quantity.quantity:
            return False

    for sauce_quantity in pizza_type.sauces:
        if sauce_quantity.sauce.stock < sauce_quantity.quantity:
            return False

    return True


def reduce_stock_of_ingredients(pizza_type: PizzaType, db: Session):
    pizza_type.dough.stock -= 1
    for topping_quantity in pizza_type.toppings:
        topping_quantity.topping.stock -= topping_quantity.quantity
    for sauce_quantity in pizza_type.sauces:
        sauce_quantity.sauce.stock -= sauce_quantity.quantity

    db.commit()


def increase_stock_of_ingredients(pizza_type: PizzaType, db: Session):
    pizza_type.dough.stock += 1

    for topping_quantity in pizza_type.toppings:
        topping_quantity.topping.stock += topping_quantity.quantity
    for sauce_quantity in pizza_type.sauces:
        sauce_quantity.sauce.stock += sauce_quantity.quantity

    db.commit()
