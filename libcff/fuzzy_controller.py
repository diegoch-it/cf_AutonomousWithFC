#         ________                   ______       __________
#        / __  /_/____ _____ ______/ ___/ /      / /__  ___/
#       / / / / / ___/ ___  / __ `/ /  / /___ __/ /  / /
#      / /_/ / / /__/ /__/ / /_/ / /__/ /-- //_/ /  / /
#     /_____/_/\___/\___  /_____/____/_/ /_/  /_/  /_/
#                   ___/ /
#                  /____/

from fuzzylogic.classes import Domain, Set, Rule
from fuzzylogic.hedges import very
from fuzzylogic.functions import bounded_sigmoid, triangular_sigmoid, gauss
from fuzzylogic.classes import rule_from_table

data_1 = 1

__author__ = 'diegoch-it'
__all__ = ['Cffuzzyc']

class Cffuzzyc:

    def __init__(self):
                
        # Universes of discourse

        self._front_range   = Domain("Front distance", 0.0, 8.0, res = 0.01)
        self._rear_range    = Domain("Back distance", 0.0, 8.0, res = 0.01)

        self._right_range   = Domain("Front distance", 0.0, 8.0, res = 0.01)
        self._left_range    = Domain("Front distance", 0.0, 8.0, res = 0.01)

        self._up_range      = Domain("Front distance", 0.0, 8.0, res = 0.01)
        self._down_range    = Domain("Front distance", 0.0, 8.0, res = 0.01)

        self._y_vel         = Domain("Longitudinal velocity", -1.0, 1.0, res = 0.01)
        self._x_vel         = Domain("Horizontal velocity", -1.0, 1.0, res = 0.01)

        self._zdistance     = Domain("Altitud on z axis", 0.0, 5.0, res = 0.01)
        self._yawrate       = Domain("Yaw rate", -25.0, 25.0, res = 0.01)

        # Input linguistic variables: Front and rear proximity sensors' membership functions

        self._front_range.far   = bounded_sigmoid(2, 3)
        self._front_range.close = bounded_sigmoid(0.18, 1, inverse=True)

        self._rear_range.far    = bounded_sigmoid(2, 3)
        self._rear_range.close  = bounded_sigmoid(0.18, 1, inverse=True)

        # Input linguistic variables: Right and left proximity sensors' membership functions

        self._right_range.far   = bounded_sigmoid(2, 4)
        self._right_range.close = bounded_sigmoid(0.18, 0.5, inverse=True)

        self._left_range.far    = bounded_sigmoid(2, 4)
        self._left_range.close  = bounded_sigmoid(0.18, 0.5, inverse=True)

        # Input linguistic variables: Up and down proximity sensors' membership functions

        self._up_range.far      = bounded_sigmoid(0.2, 1.5)
        self._up_range.close    = bounded_sigmoid(0.0, 0.25, inverse=True)

        self._down_range.far    = bounded_sigmoid(0.2, 1.5)
        self._down_range.close  = bounded_sigmoid(0.0, 0.25, inverse=True)

        # Output linguistic variables: Membership functions

        self._y_vel.forward     = bounded_sigmoid(0.4, 1)
        self._y_vel.backward    = bounded_sigmoid(-1.0, -0.4, inverse=True)

        self._x_vel.left        = bounded_sigmoid(0.5, 1)
        self._x_vel.right       = bounded_sigmoid(-1.0, -0.5, inverse=True)

        self._zdistance.up      = bounded_sigmoid(0.0, 0.5)
        self._zdistance.down    = bounded_sigmoid(0.0, 0.5)

        self._yawrate.clock     = bounded_sigmoid(-0.3, 0, inverse=True )
        self._yawrate.anticlock = bounded_sigmoid(0.0, 0.5)

    # Fuzzy inference rules, filters and defuzzification
        
    def auto(self, rfront=0, rback=0, rright=0, rleft=0, rup=0, rzrange=0):
        
        def block_saturation(d, max= 3.0):
            global data_1
            
            if d == None:
                return data_1
            elif d < max:
                data_1 = d
                return d
            else:
                return data_1 
        
        rules1 = Rule( {
                        (self._front_range.far, self._rear_range.close): self._y_vel.forward,
                        (self._rear_range.close, self._rear_range.close): self._y_vel.forward,
                        (self._front_range.close, self._front_range.close): self._y_vel.backward,
                        (self._front_range.close, self._rear_range.far): self._y_vel.backward
                        })
        
        rules2 = Rule({
                        (self._left_range.far, self._right_range.close): self._x_vel.left,
                        (self._left_range.close, self._right_range.far) : self._x_vel.right,
                        })
            
        rg1 = {
            self._front_range : block_saturation(rfront), self._rear_range : block_saturation(rback)
            }
        rg2 = {
            self._left_range : block_saturation(rleft), self._right_range : block_saturation(rright)
            }
        return [rules1(rg1), rules2(rg2)]

