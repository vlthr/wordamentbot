"""

All coordinates assume a screen resolution of 1680x1024, and wordament docked to the right side of the screen on the main monitor. 

x_pad = 1370
y_pad = 234
Play area =  x_pad+1, y_pad+1, x_pad+298, y_pad+298
"""


import win32api
import win32con
import time
import os

# Globals
# ---------------
MOUSE_MICKEYS = 65535
MICKEY_FACTOR_X = MOUSE_MICKEYS/win32api.GetSystemMetrics(0)
MICKEY_FACTOR_Y = MOUSE_MICKEYS/win32api.GetSystemMetrics(1)

def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def left_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)

def left_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)

def set_mouse(cord,jiggle=True):
    win32api.SetCursorPos((int(cord[0]), int(cord[1])))
    if jiggle: mouse_jiggle()

def mouse_jiggle():
    """
    Moves the mouse back and forth to trigger a move event
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1 , 1 )
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1 , -1 )


def move_mouse(dx,dy,jiggle=True):
    """
    Moves the mouse using a relative value

    Param x: direction of X axis movement (-1, 0, 1)
    Param y: direction of Y axis movement (-1, 0, 1)
    """
    tilePos = coords_to_tile(*get_coords())

    point_to_grid(tilePos.x + dx, tilePos.y+dy)
    if jiggle: mouse_jiggle()

    print_coords()

def move_mouse_api(x,y):
    """
    Moves the mouse using a relative value

    Param x: direction of X axis movement (-1, 0, 1)
    Param y: direction of Y axis movement (-1, 0, 1)
    """
    X, Y = get_coords()
    dX = X + (x*box_size + x*gap_size)
    dY = Y + (y*box_size + y*gap_size)
    # Win32API mouse_event takes in number of "mickeys" moved. The following converts pixels into mickeys
    dX = dX * MICKEY_FACTOR_X
    dY = dY * MICKEY_FACTOR_Y
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE, dX , dY )


    print("move_mouse: Moved to X =",dX,'and Y =',dY)
    print_coords()
