import win32gui
from PIL import ImageGrab
import math


def getImageOf(window_title, window_class, region):
    rect = getRectOf(window_title, window_class)

    image = ImageGrab.grab()

    if region:
        work = [0, 0, 0, 0]
        work[0] = region[0] + rect[0]
        work[1] = region[1] + rect[1]
        work[2] = region[2] + rect[0]
        work[3] = region[3] + rect[1]
        return image.crop(work)
    else:
        return image.crop(rect)


def getHandle(window_title, window_class):
    window_class = window_class.strip()
    window_title = window_title.strip()
    if window_class == "":
        window_class = None
    if window_title == "":
        window_title = None

    return win32gui.FindWindow(window_class, window_title)


def getRectOf(window_title, window_class):
    handle = getHandle(window_title, window_class)
    return win32gui.GetWindowRect(handle)


if __name__ == '__main__':
    image = getImageOf("電卓", "")
    image.show()
