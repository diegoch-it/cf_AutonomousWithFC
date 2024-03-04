import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator
import libcff.fuzzy_controller as Cffuzzyc

#def print3d(rfront=None, rback=None, rright=None, rleft=None, rup=None, rzrange=None):

crazy = Cffuzzyc()
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = np.arange(0, 4, 0.1)
Y = np.arange(0, 4, 0.1)
X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X ** 2 + Y ** 2)
Z = np.zeros([len(X), len(Y[0])], dtype=float)

for i in range(len(X)):
    for j in range(len(Y[i])):
        temp = crazy.auto(X[i][j], Y[i][j])
        Z[i][j] = temp[0]

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))

# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

ax.set_xlabel('Front sensor')
ax.set_ylabel('Rear sensor')
ax.set_zlabel('Setpoint')

plt.show()