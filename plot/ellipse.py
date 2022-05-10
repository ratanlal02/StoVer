import numpy as np
from numpy import linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as colors



fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')

# number of ellipsoids 
ellipNumber = 10

#set colour map so each ellipsoid as a unique colour
norm = colors.Normalize(vmin=0, vmax=ellipNumber)
cmap = cm.jet
m = cm.ScalarMappable(norm=norm, cmap=cmap)

#compute each and plot each ellipsoid iteratively
for indx in xrange(ellipNumber):
    # your ellispsoid and center in matrix form
    A = np.array([[np.random.random_sample(),0,0],
                  [0,np.random.random_sample(),0],
                  [0,0,np.random.random_sample()]])
    center = [indx*np.random.random_sample(),indx*np.random.random_sample(),indx*np.random.random_sample()]

    # find the rotation matrix and radii of the axes
    U, s, rotation = linalg.svd(A)
    c = 2
    radii = 1.0/(np.sqrt(s) * c) #reduce radii by factor 0.3 

    # calculate cartesian coordinates for the ellipsoid surface
    u = np.linspace(0.0, 2.0 * np.pi, 60)
    v = np.linspace(0.0, np.pi, 60)
    x = radii[0] * np.outer(np.cos(u), np.sin(v))
    y = radii[1] * np.outer(np.sin(u), np.sin(v))
    z = radii[2] * np.outer(np.ones_like(u), np.cos(v))

    for i in range(len(x)):
        for j in range(len(x)):
            [x[i,j],y[i,j],z[i,j]] = np.dot([x[i,j],y[i,j],z[i,j]], rotation) + center


    ax.plot_surface(x, y, z,  rstride=3, cstride=3,  color=m.to_rgba(indx), linewidth=0.1, alpha=1, shade=True)
plt.show()
