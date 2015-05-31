# Wordament bot
A simple bot that plays the windows 8 store game Wordament.

[WebM Demonstration](https://raw.githubusercontent.com/vlthr/wordamentbot/master/wordamentbot.webm)

Currently requires manually setting the following variables in Scout.py based on screen resolution:

x_pad = the x coordinate (from left) to the leftmost edge of the wordament grid.
y_pad = the y coordinate (from top) to the topmost edge of the wordament grid.
box_size = the size (in pixels) of each tile.
gap_size = the size (in pixels) of the gap between tiles.

clock_start_x = the x coordinate of the left edge of the game timer.
clock_end_x = the x coordinate of the right side of the game timer.
clock_start_y = the y coordinate of the top edge of the game timer.
clock_end_y = the y coordinate of the bottom side of the game timer.

TODO: Autodetect game area.

To start the bot, just run wordabot.py after the game starts.

## Depends
### pywin
```
pip install pywin

python C:/Python34/Scripts/pywin32_postinstall.py -install
```
### Pillow
`pip install pillow`

### Testing:
#### Nose
`pip install nose`

## Other
`Uses pytesser for OCR.`
