from PIL import Image, ImageDraw, ImageOps
from math import sin, cos, atan2

def Clear():
  return Image.new("RGBA", (1000, 1000), (0,0,0,0))

def Empty():
  return Image.new("RGBA", (1000, 1000), (0,0,0,255))

def get_t(location, direction, origin, length):
  dx = location[0] - origin[0]
  dy = location[1] - origin[1]
  vector = (cos(direction), sin(direction))
  return (dx * vector[0] + dy * vector[1]) / ((vector[0] ** 2 + vector[1] ** 2) ** 0.5) / length


def convert_to_t(colorLocation, direction, origin, length):
  return (colorLocation[0], get_t(colorLocation[1], direction, origin, length))

def minT(colorT, t):
  if len(colorT) == 0:
    return None
  if colorT[0][1] <= t:
    rest = minT(colorT[1:], t)
    if rest is None:
      return colorT[0]
    else:
      return rest
  else:
    return None

def maxT(colorT, t):
  if len(colorT) == 0:
    return None
  if colorT[0][1] >= t:
      return colorT[0]
  else:
    return maxT(colorT[1:], t)

def colorEqual(color1, color2):
  for i in range(len(color1)):
    if color1[i] != color2[i]:
      return False
  return True
  
def lerp(minColor, maxColor, pct):
  if pct <= 0:
    return minColor
  elif pct >= 100:
    return pct
  else:
    return tuple(minColor[i] * (1 - pct) + maxColor[i] * pct for i in range(len(minColor)))

def getColor(colorT, t):
  minColor = minT(colorT, t)
  maxColor = maxT(colorT, t)
  if minColor is None and maxColor is None:
    print("No colors")
    return (0, 0, 0, 0)
  elif minColor is None:
    return maxColor[0]
  elif maxColor is None:
    return minColor[0]
  else:
    if maxColor[1] == minColor[1]:
      return minColor[0]
    pct = (t - minColor[1]) / (maxColor[1] - minColor[1])
    return lerp(minColor[0], maxColor[0], pct)

def to_int(color):
  return tuple(int(i) for i in color)
def sortColorT(colorT):
  return colorT[1]

def Gradient(colorT, origin, end):
  colorT.sort(key=sortColorT)
  print(colorT)
  if len(colorT) == 1:
    image = Image.new("RGBA", (1000, 1000), colorT[0][0])
    return image
  image = Image.new("RGBA", (1000, 1000), (0,0,0,0))
  dx = end[0] - origin[0]
  dy = end[1] - origin[1]
  length = (dx ** 2 + dy ** 2) ** 0.5
  direction = atan2(dy, dx)
  for x in range(1000):
    for y in range(1000):
      image.putpixel( (x,y), to_int(getColor(colorT, get_t( ((x / 1000), 1 - (y / 1000)), direction, origin, length))))
  return image


CLEAR_BORDER_TYPE = 0
CIRCLE_BORDER_TYPE = -1
RECT_BORDER_TYPE = -2

def Border(border):
  foregroundMap = Image.new("L", (1000, 1000), 0)
  drawForeground = ImageDraw.Draw(foregroundMap)
  backgroundMap = Image.new("L", (1000, 1000), 0)
  drawBackground = ImageDraw.Draw(backgroundMap)
  if border[0] == CIRCLE_BORDER_TYPE:
    strokeWidth = border[1]
    # solid
    drawForeground.ellipse((1, 1, 999, 999), fill=255, outline=255)
    # erasing
    drawForeground.ellipse((strokeWidth + 1, strokeWidth + 1, 999 - strokeWidth, 999 - strokeWidth), fill=0, outline=0)
    drawBackground.ellipse((strokeWidth + 1, strokeWidth + 1, 999 - strokeWidth, 999 - strokeWidth), fill=255, outline=255)
  elif border[0] == RECT_BORDER_TYPE:
    strokeWidth = border[1]
    # solid
    drawForeground.rectangle((1, 1, 999, 999), fill=255, outline=255)
    # erasing
    drawForeground.rectangle((strokeWidth + 1, strokeWidth + 1, 999 - strokeWidth, 999 - strokeWidth), fill=0, outline=0)
    drawBackground.rectangle((strokeWidth + 1, strokeWidth + 1, 999 - strokeWidth, 999 - strokeWidth), fill=255, outline=255)
  else:
    radius = border[0]
    strokeWidth = border[1]
    # Full
    drawForeground.rounded_rectangle((1, 1, 999, 999), fill=255, outline=255, width=0, radius=radius)
    # Opaque
    drawForeground.rounded_rectangle((strokeWidth + 1, strokeWidth + 1, 999 - strokeWidth, 999 - strokeWidth), fill=0, outline=0, width=0, radius=radius)
    drawBackground.rounded_rectangle((strokeWidth + 1, strokeWidth + 1, 999 - strokeWidth, 999 - strokeWidth), fill=255, outline=255, width=0, radius=radius)
  return (backgroundMap, foregroundMap)

def gT0(intensity):
  if intensity == 0:
    return 0
  return 255

def threshold(image):
  mappings = image.split()
  if len(mappings) == 1:
    return image
  red = mappings[0].point(gT0)
  green = mappings[1].point(gT0)
  blue = mappings[2].point(gT0)
  return ImageOps.grayscale(Image.merge("RGB", (red, green, blue)))

def composite(image, mask):
  return Image.composite(image, Clear(), mask)

def add(image1, image2, mask):
  return Image.composite(image1, image2, mask)
  