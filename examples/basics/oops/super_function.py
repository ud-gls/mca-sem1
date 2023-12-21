class Company:
    def __init__(self, a, b):
        print("In parent class", a, b)

    def company_name(self):
        return 'Google'

class Employee(Company):
    def __init__(self, a, b, c):
        super().__init__(a, b)
        print("In child class", a, b, c)

    def info(self):
        # Calling the superclass method using super()function
        c_name = super().company_name()
        print("Jessa works at", c_name)

# Creating object of child class
emp = Employee(2 ,3, 4)
emp.info()