# Base class
class Vehicle:

    def __init__(self, name, color, price):
        self.name = name
        self.color = color
        self.price = price

    def info(self):
        print(self.name, self.color, self.price)

# Child class
class Car(Vehicle):

    def change_gear(self, no):
        print(self.name, 'change gear to number', no)

# Create object of Car
car = Car('BMW X1', 'Black', 35000)
car.info()
car.change_gear(5)
