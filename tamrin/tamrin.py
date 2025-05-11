# Singleton Pattern: Ensures only one instance of OrderManager exists
class OrderManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OrderManager, cls).__new__(cls)
            cls._instance.orders = []
        return cls._instance

    def add_order(self, order):
        self.orders.append(order)
        print(f"Order added: {order}")

    def get_orders(self):
        return self.orders

# Prototype Pattern: For cloning similar food items
from copy import deepcopy

class FoodPrototype:
    def clone(self):
        return deepcopy(self)

# Abstract Factory Pattern: For creating food collections (Italian or Mexican)
class FoodCollection:
    def create_pizza(self):
        pass

    def create_burger(self):
        pass

class ItalianFoodCollection(FoodCollection):
    def create_pizza(self):
        return Pizza("Italian Pizza", "Thin Crust", ["Olive", "Cheese"])
    
    def create_burger(self):
        return Burger("Italian Burger", ["Basil", "Mozzarella"])

class MexicanFoodCollection(FoodCollection):
    def create_pizza(self):
        return Pizza("Mexican Pizza", "Thick Crust", ["Jalapeno", "Salsa"])
    
    def create_burger(self):
        return Burger("Mexican Burger", ["Avocado", "Chili"])

# Factory Method Pattern: For selecting food type (Pizza or Burger)
class FoodFactory:
    def create_food(self):
        pass

class PizzaFactory(FoodFactory):
    def create_food(self, name="Default Pizza", crust="Thin", toppings=None):
        return Pizza(name, crust, toppings or [])

class BurgerFactory(FoodFactory):
    def create_food(self, name="Default Burger", ingredients=None):
        return Burger(name, ingredients or [])

# Builder Pattern: For customizing food items
class FoodBuilder:
    def __init__(self):
        self.food = None

    def reset(self):
        pass

    def set_name(self, name):
        pass

    def add_ingredient(self, ingredient):
        pass

    def get_food(self):
        return self.food

class PizzaBuilder(FoodBuilder):
    def __init__(self):
        self.reset()

    def reset(self):
        self.food = Pizza("Custom Pizza", "Thin", [])

    def set_name(self, name):
        self.food.name = name

    def set_crust(self, crust):
        self.food.crust = crust

    def add_ingredient(self, topping):
        self.food.toppings.append(topping)

class BurgerBuilder(FoodBuilder):
    def __init__(self):
        self.reset()

    def reset(self):
        self.food = Burger("Custom Burger", [])

    def set_name(self, name):
        self.food.name = name

    def add_ingredient(self, ingredient):
        self.food.ingredients.append(ingredient)

# Food Classes
class Pizza(FoodPrototype):
    def __init__(self, name, crust, toppings):
        self.name = name
        self.crust = crust
        self.toppings = toppings

    def __str__(self):
        return f"{self.name} with {self.crust} crust and toppings: {', '.join(self.toppings) if self.toppings else 'None'}"

    def __repr__(self):
        return self.__str__()

class Burger(FoodPrototype):
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def __str__(self):
        return f"{self.name} with ingredients: {', '.join(self.ingredients) if self.ingredients else 'None'}"

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    # Singleton: Order Manager
    order_manager = OrderManager()
    
    # Abstract Factory: Italian Food Collection
    italian_factory = ItalianFoodCollection()
    italian_pizza = italian_factory.create_pizza()
    italian_burger = italian_factory.create_burger()
    print("Italian Collection:")
    print(italian_pizza)
    print(italian_burger)
    
    # Factory Method: Create a Pizza
    pizza_factory = PizzaFactory()
    default_pizza = pizza_factory.create_food()
    print("\nFactory Method:")
    print(default_pizza)
    
    # Builder: Custom Pizza
    pizza_builder = PizzaBuilder()
    pizza_builder.set_name("Special Pizza")
    pizza_builder.set_crust("Thick")
    pizza_builder.add_ingredient("Mushroom")
    pizza_builder.add_ingredient("Pepperoni")
    custom_pizza = pizza_builder.get_food()
    print("\nBuilder:")
    print(custom_pizza)
    
    # Prototype: Clone a Pizza
    cloned_pizza = custom_pizza.clone()
    cloned_pizza.toppings.append("Extra Cheese")
    print("\nPrototype:")
    print("Original:", custom_pizza)
    print("Cloned:", cloned_pizza)
    
    # Add orders to OrderManager
    order_manager.add_order(custom_pizza)
    order_manager.add_order(cloned_pizza)
    print("\nOrders:")
    for order in order_manager.get_orders():
        print(order)