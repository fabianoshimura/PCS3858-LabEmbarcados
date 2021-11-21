#!/usr/bin/env python

import cwiid
import time

# Tutorials used for Wii plotting script:
#   http://www.raspberrypi-spy.co.uk/2013/02/nintendo-wii-remote-python-and-the-raspberry-pi/
#   http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/wiimote/
#   http://convolutedlogic.com/projects/wiimote/
#
# How to use:
#   1) Execute: "python wii-plotter.py"
#   2) Press 1 and 2 buttons together to start plotting
#   3) Press "-" and "+" buttons together to end plotting
#
class WiiPlotter():
    RED = 31
    GREEN = 32
    YELLOW = 33

    def __init__(self):
        self.interval = 0.1

    def start(self):
        print "Press 1 + 2 on your Wii remote now..."
        time.sleep(1)
        try:
            self.wii = cwiid.Wiimote()
        except RuntimeError:
            print "Error opening Wii remote connection"
            return False
        self.wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        return True

    def format(self, text, clr):
        return "\033[1;" + str(clr) + "m" + text + "\033[0m"

    # Value ranges from 0 to 72
    def plot(self, value):
        intensity = value / 24
        if intensity == 0:
            (g, y, r) = (value, 0, 0)
        elif intensity == 1:
            (g, y, r) = (24, value - 24, 0)
        else:
            (g, y, r) = (24, 24, value - 48)
        print self.format("*" * g, WiiPlotter.GREEN),
        print self.format("*" * y, WiiPlotter.YELLOW),
        print self.format("*" * r, WiiPlotter.RED)

    def finished(self):
        return (self.wii.state['buttons'] - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0)

    def dot_product_of_coords(self):
        (x, y, z) = self.wii.state['acc']
        return x*x + y*y + z*z

    def monitor(self):
        state0 = state1 = self.dot_product_of_coords()
        while not self.finished():
            value = abs(state1 - state0) / 1000
            if value > 72: value = 72
            self.plot(value)
            state0 = state1
            state1 = self.dot_product_of_coords()
            time.sleep(self.interval)

    def stop(self):
        print "\nFinished plotting..."
        self.wii.rumble = 1
        time.sleep(1)
        self.wii.rumble = 0

if __name__ == '__main__':
    wp = WiiPlotter()
    if not wp.start():
        quit()
    else:
        wp.monitor()
        wp.stop()