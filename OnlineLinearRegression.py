import numpy
from numpy import linalg 
import matplotlib.pyplot as plt

x = [[1,3],[1,5]]
y = [[3],[4]]
b = [[0],[0]]

x1 = [2,4,1,3,5,3,4,2,1,3,4,3]
y1 = [2,5,4,7,6,9,12,15,14,17,19,21]

plot_x = [x[0][1],x[1][1]]
plot_y = [y[0][0],y[1][0]]

xt_x = numpy.dot(numpy.transpose(x),x)
xt_y = numpy.dot(numpy.transpose(x),y)

temp1 = linalg.inv(xt_x)

b = numpy.dot(temp1,xt_y)

print "b : ",b
error=0

plt.axis([0, 10, 0, 1])
plt.ion()

i=0
for j in range(len(x1)-1):
    z = numpy.linspace(0, max([max(plot_x), max(plot_y)])+5)
    temp = []
#    plt.clf()  
    
    for i in range(len(z)):
	    temp.append(b[0]+b[1]*z[i])
    plt.plot(z, temp)


    plt.plot(plot_x, plot_y, 'o')
    plt.axis([min(plot_x)-3,max(plot_x)+3, min(plot_y)-3,max(plot_y)+3])
    plt.show()
    
    plot_x.append(x1[j])
    plot_y.append(y1[j])
    
    plt.pause(1)
    plt.text(x1[j], y1[j], j)  

    xt_x [0][0] += 1
    xt_x [0][1] += x1[j]
    xt_x [1][0] += x1[j]
    xt_x [1][1] += x1[j]*x1[j]

    xt_y[0][0] += y1[j]
    xt_y[1][0] += x1[j]*y1[j]

    temp1 = linalg.inv(xt_x)    

    b = numpy.dot(temp1,xt_y)
    
    print "b : ",b
