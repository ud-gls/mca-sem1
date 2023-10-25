# Base class
class Vehicle:
    def Vehicle_info(self):
        print('Inside Vehicle class')

# Child class
class Car(Vehicle):
    def car_info(self):
        print('Inside Car class')

# Child class
class SportsCar(Vehicle):
    def sports_car_info(self):
        print('Inside SportsCar class')

# Create object of SportsCar
car = Car()
s_car = SportsCar()

# access Vehicle's and Car info using SportsCar object
car.Vehicle_info()
car.car_info()
s_car.Vehicle_info()
s_car.sports_car_info()