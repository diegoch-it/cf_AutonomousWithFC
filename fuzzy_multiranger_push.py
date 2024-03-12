#/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#         ________                   ______       __________
#        / __  /_/____ _____ ______/ ___/ /      / /__  ___/
#       / / / / / ___/ ___  / __ `/ /  / /___ __/ /  / /
#      / /_/ / / /__/ /__/ / /_/ / /__/ /-- //_/ /  / /
#     /_____/_/\___/\___  /_____/____/_/ /_/  /_/  /_/
#                   ___/ /
#                  /____/
#  Copyright (C) 2024 Diego Cherioni
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
This is an implementation of the autonomous commander that allows the Crazyflie 2.1 hovering while avoiding surraunding surfaces 
and incoming mobile objects. 

The demo is ended by either pressing Ctrl-C or by holding your hand close above the
Crazyflie.

For the example to run the following hardware is needed:
 * Crazyflie 2.1
 * Crazyradio PA
 * Flow deck
 * Multiranger deck

This development is an improvement of the multiranger_push example available in https://github.com/bitcraze/crazyflie-lib-python/tree/master/examples/multiranger
"""
import logging
import sys
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper
from cflib.utils.multiranger import Multiranger
from fuzzy_controller import Cffuzzyc

cffuzz = Cffuzzyc()
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')
a = 1

if len(sys.argv) > 1:
    URI = sys.argv[1]

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def f_n(range):
    global a
    
    if range is None:
        return a
    else:
        a = float(range)
        return a
     
if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:
        with MotionCommander(scf, default_height=0.3) as motion_commander:
            with Multiranger(scf) as multiranger:
                keep_flying = True

                while keep_flying:
                    
                    velo = cffuzz.auto(f_n(multiranger.front), f_n(multiranger.back),
                                        f_n(multiranger.right), f_n(multiranger.left))
                   
                    if (f_n(multiranger.up) < 0.3):
                        keep_flying = False

                    motion_commander.start_linear_motion(
                        velo[0], velo[1], 0)

                    time.sleep(0.1)

            print('Demo terminated!')
