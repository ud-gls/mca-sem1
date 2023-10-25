class Employee:
    def __init__(self, name, salary):
        # public member
        self.name = name
        # private member
        # not accessible outside of a class
        self.__salary = salary

    def show(self):
        print("Name is ", self.name, "and salary is", self.__salary)

emp = Employee("Jessa", 40000)
emp.show()

# access salary from outside of a class
print(emp.__salary)




# Getters and Setters

# class Student:
#     def __init__(self, name, age):
#         # private member
#         self.name = name
#         self.__age = age

#     # getter method
#     def get_age(self):
#         return self.__age

#     # setter method
#     def set_age(self, age):
#         self.__age = age

# stud = Student('Jessa', 14)

# # retrieving age using getter
# print('Name:', stud.name, stud.get_age())

# # changing age using setter
# stud.set_age(16)

# # retrieving age using getter
# print('Name:', stud.name, stud.get_age())




# class Student:
#     def __init__(self, name, roll_no, age):
#         # private member
#         self.name = name
#         # private members to restrict access
#         # avoid direct data modification
#         self.__roll_no = roll_no
#         self.__age = age

#     def show(self):
#         print('Student Details:', self.name, self.__roll_no)

#     # getter methods
#     def get_roll_no(self):
#         return self.__roll_no

#     # setter method to modify data member
#     # condition to allow data modification with rules
#     def set_roll_no(self, number):
#         if number > 50:
#             print('Invalid roll no. Please set correct roll number')
#         else:
#             self.__roll_no = number

# jessa = Student('Jessa', 10, 15)

# # before Modify
# jessa.show()
# # changing roll number using setter
# jessa.set_roll_no(120)


# jessa.set_roll_no(25)
# jessa.show()



