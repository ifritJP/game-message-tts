import win32gui
from PIL import ImageGrab
import math
import sys

def getTopWindowList():
    root = win32gui.GetDesktopWindow()

    children = []
    def callback(hwnd, extra):
        try:
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                children.append(
                    [win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd)] )
        except:
            print(sys.exc_info()[0])
        return True

    try:
        win32gui.EnumWindows( callback, 0 )
    except:
        print(sys.exc_info()[0])
    return children


def getImageWith( param ):
    if param.valid_message_fix_region:
        return getImageOf(param.game_window_title, param.game_window_class,
                          param.message_fix_region)
    else:
        return getImageOf(param.game_window_title, param.game_window_class, None )
    

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
    getTopWindowList()
