#!/usr/bin/env python3

import curses

from visidata import Canvas, colors

status = 'line drawing tool'

def log_call(f, *args, **kwargs):
    global status
    strargs = map(str, args)
    if kwargs:
        strargs.append(kwargs)
    status = '%s(%s)' % (f.__name__, ', '.join(strargs))
    return f(*args, **kwargs)

def main(scr):
    global status

    colors.setup()

    scr.timeout(100)
    curses.mousemask(-1)

    c = Canvas()

    points = []

    while True:
        h, w = scr.getmaxyx()
        c.resetCanvasDimensions(*scr.getmaxyx())
        c.refresh()
        c.render_sync()

        # re-draws over entire window
        c.draw(scr)

        scr.addstr(h-1, 0, status[:w-1], 0)

        # get keystroke; timeout set above
        try:
            ch = scr.getkey()
        except curses.error:
            ch = '' # timeout

        if ch == '': continue
        if ch in ['q', '\n']: break
        elif ch == 'KEY_RIGHT': c.visibleBox.xmin -= 10
        elif ch == 'KEY_LEFT': c.visibleBox.xmin += 10
        elif ch == 'l': log_call(c.polyline, points, colors['red']); points = []
        elif ch == 'g': log_call(c.polygon, points); points = []
        elif ch == 'b': log_call(c.qcurve, points); points = []
        elif ch == '\x07': status = 'canvas=%s visible=%s' % (c.canvasBox, c.visibleBox)
        elif ch == 'KEY_MOUSE':
            devid, x, y, z, bstate = curses.getmouse()
            if bstate in [curses.BUTTON1_PRESSED, curses.BUTTON1_CLICKED]:
                points.append(c.canvasFromTerminalCoord(x,y))
            else:
                status = '(%s, %s) %s' % (x,y,bstate)
        else:
            status = ch


curses.wrapper(main)
