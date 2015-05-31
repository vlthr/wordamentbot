from PIL import ImageGrab
from wordamentbot.datatypes import AbsolutePos, RelativePos, TileCoords, Box

x_pad = 1478
y_pad = 116
box_size = 100
gap_size = 12
clock_start_x = x_pad + 292
clock_end_x = x_pad + 437
clock_start_y = 0
clock_end_y = 70

def screenGrab():
    box = (x_pad+1, y_pad+1, x_pad+298, y_pad+298)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +'.png', 'PNG')

def crop_from_image(image):
    def grab_crop(box):
        return image.crop(box)
    return grab_crop


class Scout(object):
    def __init__(self, config, grabber=None):
        self.config = config
        if grabber is None: self.grabber = crop_from_image(ImageGrab.grab())
        else: self.grabber = grabber
    def get_coords(self, absolute=True):
        """
        Returns absolute coordinates in pixels
        """
        x, y = win32api.GetCursorPos()
        if absolute:
            return AbsolutePos(x,y)
        else:
            return RelativePos(x - x_pad,y - y_pad)

    def pos_to_coords(self, xCoord,yCoord, absolute=True):
        if absolute:
            xCoord-=x_pad
            yCoord-=y_pad
        x = int(xCoord // (box_size+gap_size))
        y = int(yCoord // (box_size+gap_size))
        return TileCoords(x,y)

    def coords_to_box(self, coords, absolute=True, padding=0, pad_top=0, pad_bottom=0):
        x,y = coords
        "Returns the bounding box containing the tile at index (x,y)"
        topleft = self.coords_to_pos((x,y),absolute, middle=False)
        return Box(topleft.x + padding,  topleft.y + max(padding,pad_top), topleft.x+box_size - padding,topleft.y+box_size - max(padding, pad_bottom))
    def coords_to_pos(self, coords, absolute=True, middle=True):
        x,y = coords
        coord_x = int(x*box_size + x*gap_size + (box_size/2 if middle else 0))
        coord_y = int(y*box_size + y*gap_size + (box_size/2 if middle else 0))
        if absolute:
            return AbsolutePos(x_pad+coord_x, y_pad+coord_y)
        else:
            return RelativePos(coord_x, coord_y)
    def grab_value(self, x, y, padding=2):
        box = self.coords_to_box((x,y),padding=padding, pad_top=25)
        image = self.grabber(box)
        return image
    def grab_score(self, x, y):
        box = self.coords_to_box((x,y), pad_bottom=box_size-25)
        image = self.grabber(box)
        return image
    def grab_clock(self):
        box = Box(clock_start_x, clock_start_y, clock_end_x, clock_end_y )
        image = self.grabber(box)
        return image
    def grab_points(self):
        # TODO
        pass
    def grab_words(self):
        # TODO
        pass
