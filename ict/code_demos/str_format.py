vars = {'x':['1','2'],'y':['a','b']}
res = []
for i in vars.values()[1]:
	for j in vars.values()[0]:
		str = 'g{0}111#{1}'.format(i, j)
		res.append(str)
print res