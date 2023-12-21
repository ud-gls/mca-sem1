class Error(Exception):
    """Base class for other exceptions"""
    pass

class ValueTooSmallError(Error):
    """Raised when the input value is small"""
    pass

class ValueTooLargeError(Error):
    """Raised when the input value is large"""
    pass

while(True):
    try:
        num = int(input("Enter any value in 10 to 50 range: "))
        if num < 10:
            raise ValueTooSmallError
        elif num > 50:
            raise ValueTooLargeError
        break
    except ValueTooSmallError:
            print("Value is below range..try again")

    except ValueTooLargeError:
            print("value out of range...try again")

print("Great! value in correct range.")




# class NegativeAgeError(Exception):

#     def __init__(self, age, ):
#         message = "Age should not be negative"
#         self.age = age
#         self.message = message

# age = int(input("Enter age: "))
# if age < 0:
#     raise NegativeAgeError(age)
# # Output:
# # raise NegativeAgeError(age)
# # __main__.NegativeAgeError: -9