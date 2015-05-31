from ctypes import *
import win32con
import win32api

# START SENDINPUT TYPE DECLARATIONS
PUL = POINTER(c_ulong)
class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
             ("wScan", c_ushort),
             ("dwFlags", c_ulong),
             ("time", c_ulong),
             ("dwExtraInfo", PUL)]

class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
             ("wParamL", c_short),
             ("wParamH", c_ushort)]

class MouseInput(Structure):
    _fields_ = [("dx", c_long),
             ("dy", c_long),
             ("mouseData", c_ulong),
             ("dwFlags", c_ulong),
             ("time",c_ulong),
             ("dwExtraInfo", PUL)]

class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
              ("mi", MouseInput),
              ("hi", HardwareInput)]

class Input(Structure):
    _fields_ = [("type", c_ulong),
             ("ii", Input_I)]

class POINT(Structure):
    _fields_ = [("x", c_ulong),
             ("y", c_ulong)]
# END SENDINPUT TYPE DECLARATIONS

def SendInput_MouseMoveTo(x,y):
	"""
	Moves the mouse to the given coordinates (in mickeys)
	"""
	FInputs = Input * 2
	extra = c_ulong(0)

	move = Input_I()
	move.mi = MouseInput(c_long(x), c_long(y), 0, c_ulong(0x8000+0x0001), 0, pointer(extra))

	x = FInputs( (0, move), )
	windll.user32.SendInput(2, pointer(x), sizeof(x[0]))

