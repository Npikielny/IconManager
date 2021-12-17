from PIL import Image
from math import sin, cos, atan2

def Clear():
  return Image.new("RGBA", (1000, 1000), (0,0,0,0))

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
  image = Image.new("RGBA", (1000, 1000), (0,0,0,0))
  dx = end[0] - origin[0]
  dy = end[1] - origin[1]
  length = (dx ** 2 + dy ** 2) ** 0.5
  direction = atan2(dy, dx)
  for x in range(1000):
    for y in range(1000):
      image.putpixel( (x,y), to_int(getColor(colorT, get_t( ((x / 1000), 1 - (y / 1000)), direction, origin, length))))
  return image


