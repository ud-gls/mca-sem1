import re

txt = "The rain in India, I love India"
# x = re.findall("ai", txt)
# print(x)

# x = re.findall("Portugal", txt)
# print(x)

# x = re.search("\s", txt)

# print("The first white-space character is"
#  "located in position:", x.start())

# x = re.search("rain", txt)
# print(x.start())


# x = re.split("\s", txt)
# print(x)

# x = re.split("\s", txt, 2)
# print(x)


# x = re.sub("\s", "9", txt)
# print(x)


# x = re.search("ai", txt)
# print(x) #this will print an object

x = re.search(r"\bI\w+", txt)
print(x)
# print(x.span())
# print(x.string)
# print(x.group())






