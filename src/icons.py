import json
from os import mkdir, remove, chdir
from os.path import exists
from PIL import Image
from math import pi

from imageProcessing import Clear, Gradient

def hex_to_number(num):
    letters = ["a","b","c","d","e","f"]
    if len(num) == 0:
        return 0
    if num[0].isdigit():
        return int(num[0]) * (16 ** len(num[1:])) + hex_to_number(num[1:])
    elif num[0].lower() in letters:
        return (letters.index(num[0].lower()) + 10) * (16 ** len(num[1:])) + hex_to_number(num[1:])
    else:
        raise BaseException("Invalid character for color " + str(num[0]))

def hex_to_color(color):
    if color[0] == "#":
        color = color[1:]
    if len(color) != 6 and len(color) != 8:
        raise BaseException("Invalid color length")
    red = hex_to_number(color[0:2])
    green = hex_to_number(color[2:4])
    blue = hex_to_number(color[4:6])
    alpha = color[6:]
    if len(alpha) > 0:
        alpha = hex_to_number(alpha)
    else:
        alpha = 255
    return (red, green, blue, alpha)

def get_tuple_color(color):
    color = color.replace("(", "")
    color = color.replace(")", "")
    color = color.split(",")
    for i in color:
        if not i.isdigit():
            raise BaseException("Invalid color " + str(i))
    red = int(color[0])
    green = int(color[1])
    blue = int(color[2])
    alpha = 255
    if len(color) > 3:
        alpha = int(color[3])
    return (red, green, blue, alpha)

def get_color():
    color = None
    while color is None:
        color = input("Input color: ")
        try:
            if "," in color:
                color=get_tuple_color(color)
            else:
                color=hex_to_color(color)
                print("HEXED COLOR " + str(color))
        except Exception as e:
            print(e)
            color = None
    for c in color:
        if c < 0 or c > 255:
            raise BaseException("Invalid color, color must be between 0 and 255 (inclusive): " + str(c))

    print("RETURNING COLOR" + str(color))
    return color

def get_location():
    location = None
    print("Input origin–should be in `(x, y)` or `x, y` and should be in percent of the image width and height: ")
    while location is None:
        location = input("Input location: ").strip()
        location = location.replace("(", "")
        location = location.replace(")", "")
        location = location.split(",")
        try:
            x = float(location[0])
            y = float(location[1])
            return (x, y)
        except:
            print("Invalid location")
            location = None

def getT():
    t = None
    print("T should be decimal")
    while t is None:
        t = input("Input t: ")
        try:
            return float(t)
        except:
            t = None
            print("Invalid t")

def gradient_message():
    print("To stop adding colors, input empty.")
    print("Colors should be in hexadecimal `#FFFFFFFF` or `FFFFFFFF` or in list with commas between `(red, green, blue, alpha)` or `red, green, blue, aplha`")
    print("Alpha is always optional–will default to 255")
    print("Locations is that percent in the direction specified from the origin specified")

def get_gradient(colors=[], origin=None, end=None):
    print()
    if origin is None:
        origin = get_location()
    if end is None:
        end = get_location()
    try:
        color = get_color()
        location = getT()
        colors.append((color, location))
        print(colors)
    except Exception as e:
        print("Invalid color", e)

    if input("Would you like to add more colors? (y/n)").strip().lower() in ["yes", "y"]:
        return get_gradient(colors, origin, end)
    else:
        return Gradient(colors, origin, end)



def get_image():
    valid_inputs = ["clear", "gradient"]
    result = input(
        "Insert an image path, `clear`, or `gradient` to create a gradient: ")
    while not (result.lower() in valid_inputs or exists(result)):
        print("Invalid input–either " +
              str(valid_inputs) + " or an existing file")
        result = input(
            "Insert image: ")
    if result.lower() == "clear":
        return Clear()
    if result.lower() == "gradient":
        gradient_message()
        message = None
        gradient = None
        while message is None:
            gradient = get_gradient()
            gradient.show()
            message = input("Is this what you wanted (y/n)?")
            if not message.lower() in ["y", "yes"]:
                message = None
        return gradient
    else:
        return Image.open(result)

def create():
    chdir("themes")
    name = None
    while name is None:
        name = input("What would you like to call this theme? ")
        try:
            mkdir(name)
        except:
            print("A theme with this name already exists")
            name = None
    print()
    print("Creating theme " + name)
    print()

    # Outline
    # print("insert an image path, `clear`, or `gradient` to create a gradient")
    path = name + "/"
    # Background
    print("Please input a background")
    background = get_image()
    background.save(path + "background.png")
    # Foreground
    print("Please input a foreground")
    foreground = get_image()
    foreground.save(path + "foreground.png")
    arson()


def addMappings():
    mappings = {}
    imageName = None
    folderName = None
    with open("mappings.json") as mappingsFile:
        previousMappings = json.load(mappingsFile)
        if len(previousMappings) > 0:
            mappings = previousMappings
            print("Pre-existing mappings are: " + str(mappings))
        print("To stop mapping, input an empty image name or folder name")
    while imageName is None or imageName.strip() != "" and folderName.strip() != "":
        if not (imageName is None and folderName is None):
            mappings[folderName] = imageName
        folderName = input("Folder name: ")
        imageName = input("Template image name: ")
    with open("mappings.json", "w") as writingFile:
        writingFile.write(json.dumps(mappings))
    arson()


def deleteMappings():
    mappings = {}
    with open("mappings.json") as mappingsFile:
        previousMappings = json.load(mappingsFile)
        if len(previousMappings) > 0:
            mappings = previousMappings
            print("Pre-existing mappings are: " + str(mappings))
        else:
            print("No existing mappings to delete")
            arson()
            return
    folderName = None
    print("Stop deleting by inputting an empty name")
    while folderName is None or folderName.strip() != "":
        if not (folderName is None):
            del mappings[folderName]
        folderName = input("Folder name to delete: ")
    with open("mappings.json", "w") as deletingFile:
        deletingFile.write(json.dumps(mappings))
    arson()


def load():
    arson()


def edit():
    arson()


def simp():
    print("I don't think you need any help doing that :P")
    arson()


def quit():
    print("Have a nice evening sir ma'am")


operatives = {"create": create, "map": addMappings, "remove mapping": deleteMappings, "load": load,
              "edit": edit, "simp": simp, "quit": quit}


def arson():
    print()
    operative = input(
        "What would you like to do today? ")

    if not operative.lower() in operatives:
        print("Sadly, " + operative + " is not a valid command yet :/ ")
        print("Valid commands are: " + str(list(operatives.keys())))
        arson()
    else:
        operatives[operative]()


def onboard():
    print()
    onboardingNeeded = False
    # templates
    try:
        mkdir("templates")
        print("Generated fresh templates folder")
    except:
        pass
    # themes
    try:
        mkdir("themes")
        print("Generated fresh themes folder")
    except:
        pass
    # mappings
    if not exists("mappings.json"):
        print("It looks like we need to start mapping some images!")
        with open("mappings.json", "w") as file:
            file.write(json.dumps({"folder": "folder.png"}))
        addMappings()
        onboardingNeeded = True
    return onboardingNeeded


if __name__ == "__main__":
    print("Good morning crotophagus!")
    if not onboard():
        arson()
