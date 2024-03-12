import matplotlib.pyplot as plt
from fuzzylogic.classes import Domain, Set
from fuzzylogic.functions import (sigmoid, gauss, trapezoid, triangular, triangular_sigmoid, R, S, alpha, bounded_sigmoid)
from fuzzylogic.hedges import plus, minus, very

#--------------------------------
cas = 'leftRange' # Specify either 'frontRange', 'rearRange', 'rightRange' or 'leftRange'
#--------------------------------

# Definition of Universes of discourse  

front_range = Domain("Front distance", 0.0, 8.0, res=0.01)
rear_range= Domain("Back distance", 0.0, 8.0, res=0.01)

right_range = Domain("Right distance", 0.0, 8.0, res=0.01)
left_range = Domain("Left distance", 0.0, 8.0, res=0.01)

up_range = Domain("Up distance", 0.0, 8.0, res=0.01)
down_range = Domain("Down distance", 0.0, 8.0, res=0.01)

y_vel     = Domain("Longitudinal velocity", -1.0, 1.0, res=0.01)
x_vel     = Domain("Horizontal velocity", -1.0, 1.0, res=0.01)
zdistance = Domain("Altitud on z axis", 0.0, 5.0, res=0.01)
yawrate   = Domain("Yaw rate", -25, 25, res=0.01)


# Input linguistic variables: Front and rear membership functions
front_range.far = bounded_sigmoid(1, 3)
front_range.close = bounded_sigmoid(0.18, 1, inverse=True)

rear_range.far = bounded_sigmoid(1, 3)
rear_range.close = bounded_sigmoid(0.18, 1, inverse=True)

# Input linguistic variables: Right and left  membership functions
right_range.far = bounded_sigmoid(2, 4)
right_range.close = bounded_sigmoid(0.18, 0.5, inverse=True)

left_range.far = bounded_sigmoid(2, 4)
left_range.close = bounded_sigmoid(0.18, 0.5, inverse=True)

# Input linguistic variables: Up and down  membership functions
up_range.far = bounded_sigmoid(0.2,1.5)
up_range.close = bounded_sigmoid(0,0.5, inverse=True)

down_range.far = bounded_sigmoid(0.2,1.5)
down_range.close = bounded_sigmoid(0,0.5, inverse=True)

# Output linguistic variables: Longitudinal and vertical velocities'  membership functions

y_vel.forward =  bounded_sigmoid(0.4, 1)
y_vel.backward = bounded_sigmoid(-1, -0.4, inverse=True)

x_vel.right = bounded_sigmoid(0.5, 1)
x_vel.left = bounded_sigmoid(-1, -0.5 , inverse=True)

zdistance.up = bounded_sigmoid(0, 0.5)
zdistance.down = bounded_sigmoid(0, 0.5)

yawrate.clock     = bounded_sigmoid(-0.3, 0, inverse=True )
yawrate.anticlock = bounded_sigmoid(0, 0.5)


cases = {
    'frontRange': [front_range.far, front_range.close, y_vel.forward, y_vel.backward],
    'rearRange': [rear_range.far, rear_range.close, y_vel.forward, y_vel.backward],
    'rightRange': [right_range.far, right_range.close,  x_vel.right,  x_vel.left],
    'leftRange': [left_range.far, left_range.close,  x_vel.right,  x_vel.left],
    }
  
def plot_sets(set1a, set1b, set2a, set2b):
       
    #plt.clf()
    plt.rc("figure", figsize=(5, 5))
    plt.subplot(2, 1, 1)
    set1a.plot()
    set1b.plot() 
    label1 = '%s and %s' % (set1a, set1b)
    plt.title(label1)
    plt.subplots_adjust(hspace=0.6)
    plt.xlabel('Distance [m]')
    plt.grid()
    #plt.legend()
            
    plt.subplot(2, 1, 2)
    set2a.plot() #linewidth=2, label='forward membership f') 
    set2b.plot()#linewidth=2, label='backward membership f')
    plt.xlabel('Velocity [m/s]')
    plt.grid()
    #plt.legend()
    label2 = '%s and %s' % (set2a, set2b)
    plt.title(label2)

    plt.show()

plot_sets(cases[cas][0],cases[cas][1], cases[cas][2], cases[cas][3])