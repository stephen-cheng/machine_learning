import numpy as np

print "==============================array basic================================="
a = np.arange(15).reshape(3, 5)
print "3*5 array: ", a
print "array shape: ", a.shape
print "axes' number: ", a.ndim
print "elements' type: ", a.dtype.name
print "array size: ", a.size
print "array type: ", type(a)

print "==============================array creation================================="
a = np.array([2, 3, 5])
print "numpy array: ", a
b = np.array([(1,2,3), (4,5,6)])
print "two_dimensional array: ", b
c = np.array([[1,2], [3,4]], dtype=complex)
print "complex array: ", c
d = np.array([[1,2], [3,4]])
print "real array: ", d, d.shape
print "ones array: ", np.ones((2,3,4))
print "zeros array: ", np.zeros((3,4))
print "5 range array: ", np.arange(10,30,5)

print "==============================basic operations==============================="
a = np.arange(4)
print "raw array: ", a
print "array square: ", a**2
print "array sin: ", np.sin(a)
print "element threshold < 2: ", a<2

A = np.array([[1,1],[0,2]])
B = np.array([[2,0],[3,5]])
print "array A: ", A
print "array B: ", B
print "elementwise product: ", A*B
print "matrix product: ", A.dot(B)
print "array sum: ", A.sum()
print "array min: ", A.min()
print "sum column: ", A.sum(axis=0)
print "sum row: ", A.sum(axis=1)
print "cumulative sum each row: ", A.cumsum(axis=1)

print "==============================multidimensional array==============================="
def f(x,y):
	return 10*x+y

a = np.fromfunction(f, (4,5), dtype=int)
print "multidimensional array: ", a
print " array flat: "
for element in a.flat:
	print element

print "===============================Stacking together================================"
a = np.floor(10*np.random.random((2,2)))
b = np.floor(10*np.random.random((2,2)))
print "raw array a & b: ", a,'\n',b

print "column stacking: ", np.vstack((a,b))
print "row stacking: ", np.hstack((a,b))
	
print "================Splitting one array into several smaller ones================"
a = np.floor(10*np.random.random((3,15)))
print "raw array: ", a
print "array split 3*5: ", np.hsplit(a,3)

print "==========================shallow copy and deep copy========================="
a = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
print "raw array: ", a
b = a
print "no copy: (b is a) --> ", b is a
c = a.view()
print "shallow copy: (c is a) --> ", c is a
print "shallow copy: (c.base is a) --> ", c.base is a
c[0,3] = 1234
print "new array after shallow copy: ", a

d = a.copy()
print "deep copy: (d is a) --> ", d is a
print "deep copy: (d.base is a) --> ", d.base is a
d[0,0] = 1234
print "new array after deep copy: ", a






