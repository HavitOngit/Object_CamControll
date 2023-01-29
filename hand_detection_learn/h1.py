from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("auto")
ax.set_autoscale_on(True)


#dibujar cubo
r = [-10, 10]
for s, e in combinations(np.array(list(product(r,r,r))), 2):
    if np.sum(np.abs(s-e)) == r[1]-r[0]:
        ax.plot3D(*zip(s,e), color="b")


#dibujar punto
#ax.scatter([0],[0],[0],color="g",s=100)

d = [-2, 2]
for s, e in combinations(np.array(list(product(d,d,d))), 2):
    if np.sum(np.abs(s-e)) == d[1]-d[0]:
        ax.plot3D(*zip(s,e), color="g")

plt.show()