import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import Axes3D
import pylab
import math
#import matplotlib as mpl
from scipy.stats import multivariate_normal

def update_position(e):
    x2, y2, _ = proj3d.proj_transform(1,1,0.5, ax.get_proj())
    label.xy = x2,y2
    label.update_positions(fig.canvas.renderer)
    fig.canvas.draw()

x = np.linspace(0, 100, 100)
y = np.linspace(0, 100, 100)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))
fig = pylab.figure()



ax = fig.gca(projection='3d')
zdirs = (None, 'x', 'y', 'z', (1, 1, 0), (1, 1, 1))
ax.text(2,2,0.27, 'init', (1,1,0), color='green')
ax.text(4,4,0.16, 'lower unsafe', (0,0.3,0), color='red')
ax.text(10,10,0.135, 'upper unsafe', (0.10,1,0), color='red')
'''
x2, y2, _ = proj3d.proj_transform(1,1,0.5, ax.get_proj())

label = pylab.annotate(
    "init", 
    xy = (x2, y2), xytext = (-20, 20),
    textcoords = 'offset points', ha = 'right', va = 'bottom',
    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
#label.update_positions(fig.canvas.renderer)
fig.canvas.draw()
#fig.canvas.mpl_connect('button_release_event', update_position)
'''
#initial distribution
mu = np.array([1, 1])
cov = np.array([[1, 1],[1, 1]])
rv = multivariate_normal(mu, cov, True)
Z = rv.pdf(pos)
#ax = fig.add_subplot(111, projection='3d')
my_col = cm.jet(Z/np.amax(Z))
ax.plot_surface(X, Y, Z, rstride=1, cstride=2, facecolors = my_col,
        linewidth=1, antialiased=True)
'''
N = 3
Lmu = []
Lcov = []
for i in range(N):
	Lmu.append(np.array([math.pow(2,i+1),math.pow(2,i+1)]))
	value = 0
	if i+1>=1:
		for j in range(i):
			value+= math.pow(4,j)
		value=2*value+math.pow(4,i+1)
	else:
		value = math.pow(4,i+1)
	Lcov.append(np.array([[value+1, value],[value, value+1]]))
print Lmu
print Lcov
for i in range(N):
	rv = multivariate_normal(Lmu[i], Lcov[i], True)
	Z = rv.pdf(pos)
	#ax = fig.add_subplot(111, projection='3d')
	my_col = cm.jet(Z/np.amax(Z))
	ax.plot_surface(X, Y, Z, rstride=1, cstride=2, facecolors = my_col,linewidth=1, antialiased=True)
'''	
#unsafe distribution

mu = np.array([3, 3])
cov = np.array([[25, 25],[25, 25]])
rv = multivariate_normal(mu, cov, True)
Z = rv.pdf(pos)
#ax = fig.add_subplot(111, projection='3d')
my_col = cm.jet(Z/np.amax(Z))
ax.plot_surface(X, Y, Z, rstride=1, cstride=2, facecolors = my_col,
        linewidth=1, antialiased=True)
#ax.plot_surface(X, Y, Z)

mu = np.array([7, 7])
cov = np.array([[70, 70],[70, 70]])
rv = multivariate_normal(mu, cov, True)
Z = rv.pdf(pos)
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')

my_col = cm.jet(Z/np.amax(Z))

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors = my_col,
        linewidth=1, antialiased=True)
   
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f')
#fig.show()
fig.savefig('plot.png')
