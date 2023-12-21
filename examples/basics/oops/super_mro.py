class A:
	def __init__(self):
		print("Class A")

class B(A):
	def __init__(self):
		super(B, self).__init__()
		print("Class B")

class A1(A):
	def __init__(self):
		super(A1, self).__init__()
		print("Class A1")

class B1(A1, B):
	def __init__(self):
		super(B1, self).__init__()
		print("Class B1")


b = B1()