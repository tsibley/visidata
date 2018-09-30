#!/usr/bin/env python3

import curses
from math import sin, cos, radians

from visidata import Canvas, colors

def main(scr):
    colors.setup()

    scr.timeout(100)

    c = Canvas()

    # plotter margins can be adjusted
    c.leftMarginPixels = 0
    c.rightMarginPixels = 0
    c.topMarginPixels = 0
    c.bottomMarginPixels = 0

    zoomlevel = 1.0
    offset = 0
    while True:
        # erase previous canvas contents
        c.reset()

        # draw sin/cos with offset
        for x in range(0,360):
            c.point(x, sin(radians(x+offset)), colors['bold red'])
            c.point(x, cos(radians(x+offset)), colors['green'])

        # reset bounding box of entire canvas; will be recomputed next refresh
#        c.canvasBox = None

        # reset visible bounds of canvas; will be recomputed to be entire canvas next refresh
#        c.visibleBox = None

        # trigger refresh next draw; causes canvas to re-render to plotter
        c.refresh()

        # re-draws over entire window
        c.draw(scr)

        # get keystroke; timeout set above
        try:
            ch = scr.getkey()
        except curses.error:
            ch = '' # timeout

        if ch == 'q': break
        elif ch == '-': zoomlevel *= 1.40; c.setZoom(zoomlevel)
        elif ch == '+': zoomlevel /= 1.40; c.setZoom(zoomlevel)

        offset += 10

curses.wrapper(main)
