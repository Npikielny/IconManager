import json
from os import mkdir, remove, chdir, walk, getcwd, system
from sys import platform
from os.path import exists
from PIL import Image
from math import pi

from imageProcessing import Clear, Gradient, Border, CLEAR_BORDER_TYPE, CIRCLE_BORDER_TYPE, RECT_BORDER_TYPE, composite, threshold, add

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
            gradient = get_gradient([], None, None)
            gradient.show()
            message = input("Is this what you wanted (y/n)?")
            if not message.lower() in ["y", "yes"]:
                message = None
        return gradient
    else:
        return Image.open(result)

def get_number(message):
    value = None
    while type(value) != float or value < 0:
        value = float(input(message))
    return value

def get_border_type():
    options = { "circle": CIRCLE_BORDER_TYPE, "clear": CLEAR_BORDER_TYPE, "rectangle": RECT_BORDER_TYPE }
    border = input("Input border type (can be circle, clear, rectangle, or rounded): ")
    if border.lower() == "clear":
        return (options[border.lower()], 0)
    else:
        stroke = int(get_number("Input stroke width in percent: ") / 100 * 1000)

        if border.lower() in options:
            return (options[border.lower()], stroke)
        elif border.lower() == "rounded":
            radius = int(1000 * get_number("Input corner radius (in percent): ") / 100)
            return (radius, stroke)
        else:
            print("Invalid border type")
            return get_border_type

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
    chdir(name)
    borderType = get_border_type()
    # Background
    if borderType == CLEAR_BORDER_TYPE:
        background = Clear()
    else:
        print("Please input a background")
        background = get_image()
    # Foreground
    print("Please input a foreground")
    foreground = get_image()
    foreground.save("foreground.png")
    # Outlines
    backgroundMap, border = Border(borderType)
    backgroundMap.save("backgroundMap.png")

    background.save("background.png")
    border.save("border.png")

    chdir("..")
    chdir("..")
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

def setImage(filePath, image):
    current_path = getcwd()

    if platform == "darwin":
        # macos
        iconPath = current_path + "/" + image
        system("sips -i " + iconPath)
        system("DeRez -only icns " + iconPath + " > tmpicns.rsrc")
        system("Rez -append tmpicns.rsrc -o $'" + filePath + "/Icon\r'")
        system("SetFile -a C " + filePath)
        system("SetFile -a V $'" + filePath + "/Icon\r'")
        system("touch " + filePath)
    elif platform == "win32":
        # windows
        pass
    else:
        raise BaseException("Unimplemented")

def loadImage(image, background, foreground, outline):
    thresholdedImage = threshold(image)
    fullForeground = add(composite(foreground, thresholdedImage), outline, thresholdedImage) 
    return add(fullForeground, background, threshold(fullForeground))

def load(theme = ""):
    with open("settings.json") as settingsFile:
        settings = json.load(settingsFile)
        desktopdir = settings.get("path")
        depth = settings.get("depth")
        if desktopdir == None:
            print("Corrupted settings.json file")
            return

        with open("mappings.json") as mappingsFile:
            chdir("themes")
            while not exists(theme):
                theme = input("Input a theme: ")
            chdir(theme)
            background = Image.open("background.png")
            foreground = Image.open("foreground.png")
            border = Image.open("border.png")
            backgroundMap = Image.open("backgroundMap.png")
            background = composite(background, backgroundMap)
            templatePath = "../../templates/"
            if not exists("folder.png"):
                with Image.open(templatePath + "folder.png") as folderImage:
                    # mask = threshold(folderImage)
                    # folder = composite(foreground, mask.resize(foreground.size))
                    folder = loadImage(folderImage, Clear(), foreground, Clear())
                    folder.save("folder.png")

            folder = Image.open("folder.png")
            
            border = composite(foreground, threshold(border))

            mappings = json.load(mappingsFile)
            current_path = getcwd()
            for (roots, dirs, files) in walk(desktopdir, topdown=True):
                if roots.count("/") + 1 - desktopdir.count("/") > depth:
                    pass
                else:
                    print()
                    print(roots)
                    print()
                    for dir in dirs:
                        path = roots + "/" + dir
                        if dir in mappings:
                            imageName = mappings[dir]
                            if not exists(imageName):
                                with Image.open(templatePath + imageName) as img:
                                    icon = loadImage(img, background, foreground, border)
                                    icon.save(imageName)
                                    setImage(path, imageName)
                            else:
                                setImage(path, imageName)
                        else:
                            setImage(path, "folder.png")


        for i in [ background, foreground, border, folder, backgroundMap]:
            i.close()
        
        chdir("..")
        chdir("..")
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

    operation = operative.lower().split()

    if operative.lower() in operatives:
        operatives[operative]()
    elif len(operation) > 1 and operation[0] in operatives and operation[0] == "load":
        if operation[0] == "load":
            rest = ""
            for i in operation[1:]:
                load(rest)
    if not operative.lower() in operatives:
        print("Sadly, " + operative + " is not a valid command yet :/ ")
        print("Valid commands are: " + str(list(operatives.keys())))
        arson()


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
            print()
            file.write(json.dumps({"folder": "folder.png"}))
        onboardingNeeded = True
        addMappings()
    if not exists("settings.json"):
        with open("settings.json", "w") as settings:
            desktopDir = input("Input desktop directory path: ")
            depth = int(get_number("Input icon depth (number of folders deep the program will traverse before stopping): "))
            settings.write(json.dumps({"path": desktopDir, "depth": depth}))
        
    return onboardingNeeded


if __name__ == "__main__":
    print("Good morning crotophagus!")
    if not onboard():
        arson()
