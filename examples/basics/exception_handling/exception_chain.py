def simple_interest(amount, year, rate):
    try:
        if rate > 100:
            raise ValueError(rate)
        interest = (amount * year * rate) / 100
        print('The Simple Interest is', interest)
        return interest
    except ValueError as e:
        print('interest rate is out of range', e)

print('Case 1')
simple_interest(800, 6, 8)

print('Case 2')
simple_interest(800, 6, 800)




# try:
#     a = int(input("Enter value of a:"))
#     b = int(input("Enter value of b:"))
#     c = a/b
#     print("The answer of a divide by b:", c)
# except ZeroDivisionError as e:
#     raise ValueError("Division failed") from e