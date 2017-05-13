from math import sqrt

def multiply(a,b):
	sum_ab=0.0
	for i in range(len(a)):
		temp=a[i]*b[i]
		sum_ab+=temp
	return sum_ab

def cal_pearson(x,y):
	n=len(x)
	sum_x=sum(x)
	sum_y=sum(y)
	sum_xy=multiply(x,y)
	sum_x2 = sum([pow(i,2) for i in x])
	sum_y2 = sum([pow(j,2) for j in y])
	molecular=sum_xy-(float(sum_x)*float(sum_y)/n)
	denominator=sqrt((sum_x2-float(sum_x**2)/n)*(sum_y2-float(sum_y**2)/n))
	return molecular/denominator
	
def load_data(file):
	f=open(file,'r')
	data={}
	lines=f.readlines()
	for line in lines:
		cols=line.strip('\n').split(',')
		for i in range(len(cols)):
			data.setdefault(i,[]).append(float(cols[i]))
	x=data[0]
	y=data[1]
	return x,y

if __name__=='__main__':
	file='test.txt'
	x,y=load_data(file)
	print "x_list,y_list pearson correlation: ",str(cal_pearson(x,y))
