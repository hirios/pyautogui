# PyAutoGUI: Cross-platform GUI automation for human beings.
# BSD license
# Al Sweigart al@inventwithpython.com (Send me feedback & suggestions!)

"""
IMPORTANT NOTE!



To use this module on Windows, you do not need anything else.

You will need PIL/Pillow to use the screenshot features.
"""


# TODO - the following features are half-implemented right now:
# snapshot logging
# non-qwerty keyboard mapping
# primary secondary mouse button awareness


from __future__ import absolute_import, division, print_function


__version__ = "0.9.48"

import sys
import time
import datetime
import os
import platform
import re

from .keynames import KEY_NAMES

class PyAutoGUIException(Exception):
    pass


class FailSafeException(PyAutoGUIException):
    pass


if sys.version_info[0] == 2 or sys.version_info[0:2] in ((3, 1), (3, 2)):
    # Python 2 and 3.1 and 3.2 uses collections.Sequence
    import collections

    collectionsSequence = collections.Sequence
else:
    # Python 3.3+ uses collections.abc.Sequence
    import collections.abc

    collectionsSequence = collections.abc.Sequence


try:
    import pytweening
    from pytweening import (
        easeInQuad,
        easeOutQuad,
        easeInOutQuad,
        easeInCubic,
        easeOutCubic,
        easeInOutCubic,
        easeInQuart,
        easeOutQuart,
        easeInOutQuart,
        easeInQuint,
        easeOutQuint,
        easeInOutQuint,
        easeInSine,
        easeOutSine,
        easeInOutSine,
        easeInExpo,
        easeOutExpo,
        easeInOutExpo,
        easeInCirc,
        easeOutCirc,
        easeInOutCirc,
        easeInElastic,
        easeOutElastic,
        easeInOutElastic,
        easeInBack,
        easeOutBack,
        easeInOutBack,
        easeInBounce,
        easeOutBounce,
        easeInOutBounce,
    )

    # getLine is not needed.
    # getPointOnLine has been redefined in this file, to avoid dependency on pytweening.
    # linear has also been redefined in this file.
except ImportError:

    def couldNotImportPyTweening():
        raise PyAutoGUIException(
            "PyAutoGUI was unable to import pytweening. Please install this module to enable the function you tried to call."
        )
        easeInQuad = couldNotImportPyTweening
        easeOutQuad = couldNotImportPyTweening
        easeInOutQuad = couldNotImportPyTweening
        easeInCubic = couldNotImportPyTweening
        easeOutCubic = couldNotImportPyTweening
        easeInOutCubic = couldNotImportPyTweening
        easeInQuart = couldNotImportPyTweening
        easeOutQuart = couldNotImportPyTweening
        easeInOutQuart = couldNotImportPyTweening
        easeInQuint = couldNotImportPyTweening
        easeOutQuint = couldNotImportPyTweening
        easeInOutQuint = couldNotImportPyTweening
        easeInSine = couldNotImportPyTweening
        easeOutSine = couldNotImportPyTweening
        easeInOutSine = couldNotImportPyTweening
        easeInExpo = couldNotImportPyTweening
        easeOutExpo = couldNotImportPyTweening
        easeInOutExpo = couldNotImportPyTweening
        easeInCirc = couldNotImportPyTweening
        easeOutCirc = couldNotImportPyTweening
        easeInOutCirc = couldNotImportPyTweening
        easeInElastic = couldNotImportPyTweening
        easeOutElastic = couldNotImportPyTweening
        easeInOutElastic = couldNotImportPyTweening
        easeInBack = couldNotImportPyTweening
        easeOutBack = couldNotImportPyTweening
        easeInOutBack = couldNotImportPyTweening
        easeInBounce = couldNotImportPyTweening
        easeOutBounce = couldNotImportPyTweening
        easeInOutBounce = couldNotImportPyTweening


try:
    import pymsgbox
    from pymsgbox import alert, confirm, prompt, password
except ImportError:
    # If pymsgbox module is not found, those methods will not be available.
    def couldNotImportPyMsgBox():
        raise PyAutoGUIException(
            "PyAutoGUI was unable to import pymsgbox. Please install this module to enable the function you tried to call."
        )

    alert = confirm = prompt = password = couldNotImportPyMsgBox


try:
    import pyscreeze
    from pyscreeze import (
        center,
        grab,
        locate,
        locateAll,
        locateAllOnScreen,
        locateCenterOnScreen,
        locateOnScreen,
        pixel,
        pixelMatchesColor,
        screenshot,
    )
except ImportError:
    # If pyscreeze module is not found, screenshot-related features will simply not work.
    def couldNotImportPyScreeze():
        raise PyAutoGUIException(
            "PyAutoGUI was unable to import pyscreeze. (This is likely because you're running a version of Python that Pillow (which pyscreeze depends on) doesn't support currently.) Please install this module to enable the function you tried to call."
        )

        center = couldNotImportPyScreeze
        grab = couldNotImportPyScreeze
        locate = couldNotImportPyScreeze
        locateAll = couldNotImportPyScreeze
        locateAllOnScreen = couldNotImportPyScreeze
        locateCenterOnScreen = couldNotImportPyScreeze
        locateOnScreen = couldNotImportPyScreeze
        pixel = couldNotImportPyScreeze
        pixelMatchesColor = couldNotImportPyScreeze
        screenshot = couldNotImportPyScreeze


try:
    import mouseinfo

    def mouseInfo():
        mouseinfo.MouseInfoWindow()


except ImportError:

    def mouseInfo():
        raise PyAutoGUIException(
            "PyAutoGUI was unable to import mouseinfo. Please install this module to enable the function you tried to call."
        )


def useImageNotFoundException(value=None):
    if value is None:
        value = True
    # TODO - this will cause a NameError if PyScreeze couldn't be imported:
    pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = value


if sys.platform == "win32":  # PyGetWindow currently only supports Windows.
    try:
        import pygetwindow
        from pygetwindow import (
            Window,
            getActiveWindow,
            getActiveWindowTitle,
            getWindowsAt,
            getWindowsWithTitle,
            getAllWindows,
            getAllTitles,
        )
    except ImportError:
        # If pygetwindow module is not found, those methods will not be available.
        def couldNotImportPyGetWindow():
            raise PyAutoGUIException(
                "PyAutoGUI was unable to import pygetwindow. Please install this module to enable the function you tried to call."
            )

        Window = couldNotImportPyGetWindow
        getActiveWindow = couldNotImportPyGetWindow
        getActiveWindowTitle = couldNotImportPyGetWindow
        getWindowsAt = couldNotImportPyGetWindow
        getWindowsWithTitle = couldNotImportPyGetWindow
        getAllWindows = couldNotImportPyGetWindow
        getAllTitles = couldNotImportPyGetWindow


KEYBOARD_KEYS = KEY_NAMES  # keeping old KEYBOARD_KEYS for backwards compatibility

# Constants for the mouse button names:
LEFT = "left"
MIDDLE = "middle"
RIGHT = "right"
PRIMARY = "primary"
SECONDARY = "secondary"

# Different keyboard mappings:
# TODO - finish this feature.
# NOTE: Eventually, I'd like to come up with a better system than this. For now, this seems like it works.
QWERTY = r"""`1234567890-=qwertyuiop[]\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?"""
QWERTZ = r"""=1234567890/0qwertzuiop89-asdfghjkl,\yxcvbnm,.7+!@#$%^&*()?)QWERTZUIOP*(_ASDFGHJKL<|YXCVBNM<>&"""


def isShiftCharacter(character):
    """Returns True if the key character is uppercase or shifted."""
    return character.isupper() or character in '~!@#$%^&*()_+{}|:"<>?'


# The platformModule is where we reference the platform-specific functions.
if sys.platform.startswith("java"):
    # from . import _pyautogui_java as platformModule
    raise NotImplementedError("Jython is not yet supported by PyAutoGUI.")
elif sys.platform == "darwin":
    from . import _pyautogui_osx as platformModule
elif sys.platform == "win32":
    from . import _pyautogui_win as platformModule
elif platform.system() == "Linux":
    from . import _pyautogui_x11 as platformModule
else:
    raise NotImplementedError("Your platform (%s) is not supported by PyAutoGUI." % (platform.system()))

# TODO: Having module-wide user-writable global variables is bad. It makes
# restructuring the code very difficult. For instance, what if we decide to
# move the mouse-related functions to a separate file (a submodule)? How that
# file will access this module vars? It will probably lead to a circular
# import.

# In seconds. Any duration less than this is rounded to 0.0 to instantly move
# the mouse.
MINIMUM_DURATION = 0.1
# If sleep_amount is less than MINIMUM_DURATION, time.sleep() will be a no-op and the mouse cursor moves there instantly.
# TODO: This value should vary with the platform. http://stackoverflow.com/q/1133857
MINIMUM_SLEEP = 0.05
PAUSE = 0.1  # The number of seconds to pause after EVERY public function call. Useful for debugging.


# If the mouse is over a coordinate in FAILSAFE_POINTS and FAILSAFE is True, the FailSafeException is raised.
# The rest of the points are added to the FAILSAFE_POINTS list at the bottom of this file, after size() has been defined.
# The points are for the corners of the screen, but note that these points don't automatically change if the screen resolution changes.
FAILSAFE = True
FAILSAFE_POINTS = [(0, 0)]

LOG_SCREENSHOTS = False  # If True, save screenshots for clicks and key presses.
LOG_SCREENSHOTS_LIMIT = 10  # If not None, PyAutoGUI deletes old screenshots when this limit has been reached.
G_LOG_SCREENSHOTS_FILENAMES = []  # TODO - make this a deque

Point = collections.namedtuple("Point", "x y")
Size = collections.namedtuple("Size", "width height")


# General Functions
# =================


def getPointOnLine(x1, y1, x2, y2, n):
    """Returns the (x, y) tuple of the point that has progressed a proportion
    n along the line defined by the two x, y coordinates.

    Copied from pytweening module.
    """
    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1
    return (x, y)


def linear(n):
    """Trivial linear tweening function.

    Copied from pytweening module.
    """

    # We use this function instead of pytweening.linear for the default tween function just in case pytweening couldn't be imported.
    if not 0.0 <= n <= 1.0:
        raise ValueError("Argument must be between 0.0 and 1.0.")
    return n


def _autoPause(pause, _pause):
    """If `pause` is not `None`, then sleep for `pause` seconds.
    If `_pause` is `True`, then sleep for `PAUSE` seconds (the global pause setting).

    This function is called at the end of all of PyAutoGUI's mouse and keyboard functions. Normally, `_pause`
    is set to `True` to add a short sleep so that the user can engage the failsafe. By default, this sleep
    is as long as `PAUSE` settings. However, this can be override by setting `pause`, in which case the sleep
    is as long as `pause` seconds.
    """
    if pause is not None:
        time.sleep(pause)
    elif _pause:
        assert isinstance(PAUSE, int) or isinstance(PAUSE, float)
        time.sleep(PAUSE)


def _unpackXY(x, y):
    """If x is a sequence and y is None, returns x[0], y[0]. Else, returns x, y.

    On functions that receive a pair of x,y coordinates, they can be passed as
    separate arguments, or as a single two-element sequence.
    """
    if isinstance(x, str):
        # x parameter is the string of an image filename to find and click on:
        x, y = center(locateOnScreen(x))

    elif isinstance(x, collectionsSequence):
        if len(x) == 2:
            # x is a two-integer tuple: (x, y)
            if y is None:
                x, y = x
            else:
                raise ValueError(
                    "When passing a sequence as the x argument, the y argument must not be passed (received {0}).".format(
                        repr(y)
                    )
                )
        elif len(x) == 4:
            # x is a four-integer tuple: (left, top, width, height)
            if y is None:
                x, y = center(x)
            else:
                raise ValueError(
                    "When passing a sequence as the x argument, the y argument must not be passed (received {0}).".format(
                        repr(y)
                    )
                )
        else:
            raise ValueError(
                "The supplied sequence must have exactly 2 or exactly 4 elements ({0} were received).".format(len(x))
            )
    else:
        pass  # x and y are just number values

    return x, y


def _logScreenshot(logScreenshot, action, specifics, folder="."):
    if logScreenshot == False:
        return  # Don't take a screenshot.
    if logScreenshot is None and LOG_SCREENSHOTS == False:
        return  # Don't take a screenshot.

    # Ensure that the "specifics" string isn't too long for the filename:
    if len(specifics) > 12:
        specifics = specifics[:12] + "..."

    now = datetime.datetime.now()
    filename = "%s-%s-%s_%s-%s-%s-%s_%s_%s.png" % (
        now.year,
        str(now.month).rjust(2, "0"),
        str(now.day).rjust(2, "0"),
        now.hour,
        now.minute,
        now.second,
        str(now.microsecond)[:3],
        action,
        specifics,
    )
    filepath = os.path.join(folder, filename)

    # Delete the oldest screenshot if we've reached the maximum:
    if (LOG_SCREENSHOTS_LIMIT is not None) and (len(G_LOG_SCREENSHOTS_FILENAMES) >= LOG_SCREENSHOTS_LIMIT):
        os.unlink(os.path.join(folder, G_LOG_SCREENSHOTS_FILENAMES[0]))
        del G_LOG_SCREENSHOTS_FILENAMES[0]

    screenshot(filepath)
    G_LOG_SCREENSHOTS_FILENAMES.append(filename)


def position(x=None, y=None):
    """Returns the current xy coordinates of the mouse cursor as a two-integer
    tuple.

    Args:
      x (int, None, optional) - If not None, this argument overrides the x in
        the return value.
      y (int, None, optional) - If not None, this argument overrides the y in
        the return value.

    Returns:
      (x, y) tuple of the current xy coordinates of the mouse cursor.

    NOTE: The position() functon doesn't check for failsafe.
    """
    posx, posy = platformModule._position()
    posx = int(posx)
    posy = int(posy)
    if x is not None:  # If set, the x parameter overrides the return value.
        posx = int(x)
    if y is not None:  # If set, the y parameter overrides the return value.
        posy = int(y)
    return Point(posx, posy)


def size():
    """Returns the width and height of the screen as a two-integer tuple.

    Returns:
      (width, height) tuple of the screen size, in pixels.
    """
    return Size(*platformModule._size())


def onScreen(x, y=None):
    """Returns whether the given xy coordinates are on the primary screen or not.

    Note that this function doesn't work for secondary screens.

    Args:
      Either the arguments are two separate values, first arg for x and second
        for y, or there is a single argument of a sequence with two values, the
        first x and the second y.
        Example: onScreen(x, y) or onScreen([x, y])

    Returns:
      bool: True if the xy coordinates are on the screen at its current
        resolution, otherwise False.
    """
    x, y = _unpackXY(x, y)
    x = int(x)
    y = int(y)

    width, height = platformModule._size()
    return 0 <= x < width and 0 <= y < height


# Mouse Functions
# ===============

"""
NOTE: Although "mouse1" and "mouse2" buttons usually refer to the left and
right mouse buttons respectively, in PyAutoGUI 1, 2, and 3 refer to the left,
middle, and right buttons, respectively. This is because Xlib interprets
button 2 as the middle button and button 3 as the right button, so we hold
that for Windows and macOS as well (since those operating systems don't use
button numbers but rather just "left" or "right").
"""


def _translateButton(button):
    """
    The left, middle, and right mouse buttons are button numbers 1, 2, and 3
    respectively. This is the numbering that Xlib on Linux uses (while Windows
    and macOS don't care about numbers; they just use "left" and "right").

    The 'left' and 'right' mouse buttons will always refer to the physical
    buttons on the mouse. The same applies for button 1 and 3.

    However, if `button` is 'primary' or 'secondary', then we must check if
    the mouse buttons have been "swapped" by the operating system's mouse
    settings. If not swapped, the primary and secondary buttons are the left
    and right mouse buttons respectively, and if swapped, the primary and
    secondary buttons are the right and left mouse buttons, respectively.

    TODO - The swap detection hasn't been done yet.
    """
    # TODO - We should check the OS settings to see if it's a left-hand setup, where button 1 would be "right".

    # Check that `button` has a valid value:
    button = button.lower()
    if platform.system() == "Linux":
        # Check for valid button arg on Linux:
        if button not in (LEFT, MIDDLE, RIGHT, PRIMARY, SECONDARY, 1, 2, 3, 4, 5, 6, 7):
            raise ValueError(
                "button argument must be one of ('left', 'middle', 'right', 'primary', 'secondary', 1, 2, 3, 4, 5, 6, 7)"
            )
    else:
        # Check for valid button arg on Windows and macOS:
        if button not in (LEFT, MIDDLE, RIGHT, PRIMARY, SECONDARY, 1, 2, 3):
            raise ValueError(
                "button argument must be one of ('left', 'middle', 'right', 'primary', 'secondary', 1, 2, 3)"
            )

    # TODO - Check if the primary/secondary mouse buttons have been swapped:
    if button in (PRIMARY, SECONDARY):
        swapped = False  # TODO - Add the operating system-specific code to detect mouse swap later.
        if swapped:
            if button == PRIMARY:
                return RIGHT
            elif button == SECONDARY:
                return LEFT
        else:
            if button == PRIMARY:
                return LEFT
            elif button == SECONDARY:
                return RIGHT

    # Return a mouse button integer value, not a string like 'left':
    return {LEFT: LEFT, MIDDLE: MIDDLE, RIGHT: RIGHT, 1: LEFT, 2: MIDDLE, 3: RIGHT, 4: 4, 5: 5, 6: 6, 7: 7}[button]


def mouseDown(x=None, y=None, button=PRIMARY, duration=0.0, tween=linear, pause=None, logScreenshot=None, _pause=True):
    """Performs pressing a mouse button down (but not up).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        mouse down happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        mouse down happens. None by default.
      button (str, int, optional): The mouse button pressed down. TODO

    Returns:
      None

    Raises:
      ValueError: If button is not one of 'left', 'middle', 'right', 1, 2, or 3
    """
    button = _translateButton(button)
    failSafeCheck()
    x, y = _unpackXY(x, y)

    _mouseMoveDrag("move", x, y, 0, 0, duration=0, tween=None)

    x, y = platformModule._position()  # TODO Why do we call _position() here and overwrite x, y?
    _logScreenshot(logScreenshot, "mouseDown", "%s,%s" % (x, y), folder=".")
    platformModule._mouseDown(x, y, button)

    _autoPause(pause, _pause)


def mouseUp(x=None, y=None, button=PRIMARY, duration=0.0, tween=linear, pause=None, logScreenshot=None, _pause=True):
    """Performs releasing a mouse button up (but not down beforehand).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        mouse up happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        mouse up happens. None by default.
      button (str, int, optional): The mouse button released. TODO

    Returns:
      None

    Raises:
      ValueError: If button is not one of 'left', 'middle', 'right', 1, 2, or 3
    """
    button = _translateButton(button)
    failSafeCheck()
    x, y = _unpackXY(x, y)

    _mouseMoveDrag("move", x, y, 0, 0, duration=0, tween=None)

    x, y = platformModule._position()  # TODO Why do we call _position() here and overwrite x, y?
    _logScreenshot(logScreenshot, "mouseUp", "%s,%s" % (x, y), folder=".")
    platformModule._mouseUp(x, y, button)

    _autoPause(pause, _pause)


def click(
    x=None,
    y=None,
    clicks=1,
    interval=0.0,
    button=PRIMARY,
    duration=0.0,
    tween=linear,
    pause=None,
    logScreenshot=None,
    _pause=True,
):
    """Performs pressing a mouse button down and then immediately releasing it.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, str, optional): The x position on the screen where
        the click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.
      clicks (int, optional): The number of clicks to perform. 1 by default.
        For example, passing 2 would do a doubleclick.
      interval (float, optional): The number of seconds in between each click,
        if the number of clicks is greater than 1. 0.0 by default, for no
        pause in between clicks.
      button (str, int, optional): The mouse button clicked. TODO

    Returns:
      None

    Raises:
      ValueError: If button is not one of 'left', 'middle', 'right', 1, 2, 3
    """
    button = _translateButton(button)
    failSafeCheck()
    x, y = _unpackXY(x, y)

    _mouseMoveDrag("move", x, y, 0, 0, duration, tween)

    x, y = platformModule._position()  # TODO Why do we call _position() here and overwrite x, y?

    _logScreenshot(logScreenshot, "click", "%s,%s,%s,%s" % (button, clicks, x, y), folder=".")

    if sys.platform == 'darwin':
        for i in range(clicks):
            _failSafeCheck()
            if button in (LEFT, MIDDLE, RIGHT):
                platformModule._multiClick(x, y, button, 1, interval)
    else:
        for i in range(clicks):
            failSafeCheck()
            if button in (LEFT, MIDDLE, RIGHT):
                platformModule._click(x, y, button)

            time.sleep(interval)

    _autoPause(pause, _pause)


def leftClick(x=None, y=None, interval=0.0, duration=0.0, tween=linear, pause=None, logScreenshot=None, _pause=True):
    """Performs a right mouse button click.

    This is a wrapper function for click('right', x, y).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.
      interval (float, optional): The number of seconds in between each click,
        if the number of clicks is greater than 1. 0.0 by default, for no
        pause in between clicks.

    Returns:
      None
    """
    failSafeCheck()
    click(x, y, 1, interval, LEFT, duration, tween, pause, logScreenshot, _pause=_pause)
    _autoPause(pause, _pause)


def rightClick(x=None, y=None, interval=0.0, duration=0.0, tween=linear, pause=None, logScreenshot=None, _pause=True):
    """Performs a right mouse button click.

    This is a wrapper function for click('right', x, y).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.
      interval (float, optional): The number of seconds in between each click,
        if the number of clicks is greater than 1. 0.0 by default, for no
        pause in between clicks.

    Returns:
      None
    """
    failSafeCheck()
    click(x, y, 1, interval, RIGHT, duration, tween, pause, logScreenshot, _pause=_pause)
    _autoPause(pause, _pause)


def middleClick(x=None, y=None, interval=0.0, duration=0.0, tween=linear, pause=None, logScreenshot=None, _pause=True):
    """Performs a middle mouse button click.

    This is a wrapper function for click('right', x, y).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.

    Returns:
      None
    """
    failSafeCheck()
    click(x, y, 1, interval, MIDDLE, duration, tween, pause, logScreenshot, _pause=_pause)
    _autoPause(pause, _pause)


def doubleClick(
    x=None, y=None, interval=0.0, button=LEFT, duration=0.0, tween=linear, pause=None, logScreenshot=None, _pause=True
):
    """Performs a double click.

    This is a wrapper function for click('left', x, y, 2, interval).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.
      interval (float, optional): The number of seconds in between each click,
        if the number of clicks is greater than 1. 0.0 by default, for no
        pause in between clicks.
      button (str, int, optional): The mouse button released. TODO

    Returns:
      None

    Raises:
      ValueError: If button is not one of 'left', 'middle', 'right', 1, 2, 3, 4,
        5, 6, or 7
    """
    failSafeCheck()

    # Multiple clicks work different in OSX
    if sys.platform == "darwin":
        x, y = _unpackXY(x, y)
        _mouseMoveDrag("move", x, y, 0, 0, duration=0, tween=None)
        x, y = platformModule._position()
        _logScreenshot(logScreenshot, "click", "%s,2,%s,%s" % (button, x, y), folder=".")
        platformModule._multiClick(x, y, button, 2)
    else:
        # Click for Windows or Linux:
        click(x, y, 2, interval, button, duration, tween, pause, logScreenshot, _pause=False)

    _autoPause(pause, _pause)


def tripleClick(
    x=None, y=None, interval=0.0, button=LEFT, duration=0.0, tween=linear, pause=None, logScreenshot=None, _pause=True
):
    """Performs a triple click..

    This is a wrapper function for click('left', x, y, 3, interval).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.
      interval (float, optional): The number of seconds in between each click,
        if the number of clicks is greater than 1. 0.0 by default, for no
        pause in between clicks.
      button (str, int, optional): The mouse button released. TODO

    Returns:
      None

    Raises:
      ValueError: If button is not one of 'left', 'middle', 'right', 1, 2, 3, 4,
        5, 6, or 7
    """
    failSafeCheck()

    # Multiple clicks work different in OSX
    if sys.platform == "darwin":
        x, y = _unpackXY(x, y)
        _mouseMoveDrag("move", x, y, 0, 0, duration=0, tween=None)
        x, y = platformModule._position()
        _logScreenshot(logScreenshot, "click", "%s,3,%s,%s" % (x, y), folder=".")
        platformModule._multiClick(x, y, button, 3)
    else:
        # Click for Windows or Linux:
        click(x, y, 3, interval, button, duration, tween, pause, logScreenshot, _pause=False)
    _autoPause(pause, _pause)


def scroll(clicks, x=None, y=None, pause=None, logScreenshot=None, _pause=True):
    """Performs a scroll of the mouse scroll wheel.

    Whether this is a vertical or horizontal scroll depends on the underlying
    operating system.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      clicks (int, float): The amount of scrolling to perform.
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.

    Returns:
      None
    """
    failSafeCheck()
    if type(x) in (tuple, list):
        x, y = x[0], x[1]
    x, y = position(x, y)

    _logScreenshot(logScreenshot, "scroll", "%s,%s,%s" % (clicks, x, y), folder=".")
    platformModule._scroll(clicks, x, y)

    _autoPause(pause, _pause)


def hscroll(clicks, x=None, y=None, pause=None, logScreenshot=None, _pause=True):
    """Performs an explicitly horizontal scroll of the mouse scroll wheel,
    if this is supported by the operating system. (Currently just Linux.)

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      clicks (int, float): The amount of scrolling to perform.
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.

    Returns:
      None
    """
    failSafeCheck()
    if type(x) in (tuple, list):
        x, y = x[0], x[1]
    x, y = position(x, y)

    _logScreenshot(logScreenshot, "hscroll", "%s,%s,%s" % (clicks, x, y), folder=".")
    platformModule._hscroll(clicks, x, y)

    _autoPause(pause, _pause)


def vscroll(clicks, x=None, y=None, pause=None, logScreenshot=None, _pause=True):
    """Performs an explicitly vertical scroll of the mouse scroll wheel,
    if this is supported by the operating system. (Currently just Linux.)

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      clicks (int, float): The amount of scrolling to perform.
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.

    Returns:
      None
    """
    failSafeCheck()
    if type(x) in (tuple, list):
        x, y = x[0], x[1]
    x, y = position(x, y)

    _logScreenshot(logScreenshot, "vscroll", "%s,%s,%s" % (clicks, x, y), folder=".")
    platformModule._vscroll(clicks, x, y)

    _autoPause(pause, _pause)


def moveTo(x=None, y=None, duration=0.0, tween=linear, pause=None, logScreenshot=False, _pause=True):
    """Moves the mouse cursor to a point on the screen.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.
      duration (float, optional): The amount of time it takes to move the mouse
        cursor to the xy coordinates. If 0, then the mouse cursor is moved
        instantaneously. 0.0 by default.
      tween (func, optional): The tweening function used if the duration is not
        0. A linear tween is used by default.

    Returns:
      None
    """
    failSafeCheck()
    x, y = _unpackXY(x, y)

    _logScreenshot(logScreenshot, "moveTo", "%s,%s" % (x, y), folder=".")
    _mouseMoveDrag("move", x, y, 0, 0, duration, tween)

    _autoPause(pause, _pause)


def moveRel(xOffset=None, yOffset=None, duration=0.0, tween=linear, pause=None, logScreenshot=False, _pause=True):
    """Moves the mouse cursor to a point on the screen, relative to its current
    position.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): How far left (for negative values) or
        right (for positive values) to move the cursor. 0 by default. If tuple, this is used for x and y.
      y (int, float, None, optional): How far up (for negative values) or
        down (for positive values) to move the cursor. 0 by default.
      duration (float, optional): The amount of time it takes to move the mouse
        cursor to the new xy coordinates. If 0, then the mouse cursor is moved
        instantaneously. 0.0 by default.
      tween (func, optional): The tweening function used if the duration is not
        0. A linear tween is used by default.

    Returns:
      None
    """

    failSafeCheck()

    xOffset, yOffset = _unpackXY(xOffset, yOffset)

    _logScreenshot(logScreenshot, "moveRel", "%s,%s" % (xOffset, yOffset), folder=".")
    _mouseMoveDrag("move", None, None, xOffset, yOffset, duration, tween)

    _autoPause(pause, _pause)


move = moveRel  # For PyAutoGUI 1.0, move() replaces moveRel().


def dragTo(
    x=None,
    y=None,
    duration=0.0,
    tween=linear,
    button=PRIMARY,
    pause=None,
    logScreenshot=None,
    _pause=True,
    mouseDownUp=True,
):
    """Performs a mouse drag (mouse movement while a button is held down) to a
    point on the screen.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): How far left (for negative values) or
        right (for positive values) to move the cursor. 0 by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): How far up (for negative values) or
        down (for positive values) to move the cursor. 0 by default.
      duration (float, optional): The amount of time it takes to move the mouse
        cursor to the new xy coordinates. If 0, then the mouse cursor is moved
        instantaneously. 0.0 by default.
      tween (func, optional): The tweening function used if the duration is not
        0. A linear tween is used by default.
      button (str, int, optional): The mouse button released. TODO
      mouseDownUp (True, False): When true, the mouseUp/Down actions are not perfomed.
        Which allows dragging over multiple (small) actions. 'True' by default.

    Returns:
      None
    """
    failSafeCheck()
    x, y = _unpackXY(x, y)

    _logScreenshot(logScreenshot, "dragTo", "%s,%s" % (x, y), folder=".")
    if mouseDownUp:
        mouseDown(button=button, logScreenshot=False, _pause=False)
    _mouseMoveDrag("drag", x, y, 0, 0, duration, tween, button)
    if mouseDownUp:
        mouseUp(button=button, logScreenshot=False, _pause=False)

    _autoPause(pause, _pause)


def dragRel(
    xOffset=0,
    yOffset=0,
    duration=0.0,
    tween=linear,
    button=PRIMARY,
    pause=None,
    logScreenshot=None,
    _pause=True,
    mouseDownUp=True,
):
    """Performs a mouse drag (mouse movement while a button is held down) to a
    point on the screen, relative to its current position.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): How far left (for negative values) or
        right (for positive values) to move the cursor. 0 by default. If tuple, this is used for xOffset and yOffset.
      y (int, float, None, optional): How far up (for negative values) or
        down (for positive values) to move the cursor. 0 by default.
      duration (float, optional): The amount of time it takes to move the mouse
        cursor to the new xy coordinates. If 0, then the mouse cursor is moved
        instantaneously. 0.0 by default.
      tween (func, optional): The tweening function used if the duration is not
        0. A linear tween is used by default.
      button (str, int, optional): The mouse button released. TODO
      mouseDownUp (True, False): When true, the mouseUp/Down actions are not perfomed.
        Which allows dragging over multiple (small) actions. 'True' by default.

    Returns:
      None
    """
    if xOffset is None:
        xOffset = 0
    if yOffset is None:
        yOffset = 0

    if type(xOffset) in (tuple, list):
        xOffset, yOffset = xOffset[0], xOffset[1]

    if xOffset == 0 and yOffset == 0:
        return  # no-op case

    failSafeCheck()

    mousex, mousey = platformModule._position()
    _logScreenshot(logScreenshot, "dragRel", "%s,%s" % (xOffset, yOffset), folder=".")
    if mouseDownUp:
        mouseDown(button=button, logScreenshot=False, _pause=False)
    _mouseMoveDrag("drag", mousex, mousey, xOffset, yOffset, duration, tween, button)
    if mouseDownUp:
        mouseUp(button=button, logScreenshot=False, _pause=False)

    _autoPause(pause, _pause)


drag = dragRel  # For PyAutoGUI 1.0, we want drag() to replace dragRel().


def _mouseMoveDrag(moveOrDrag, x, y, xOffset, yOffset, duration, tween=linear, button=None):
    """Handles the actual move or drag event, since different platforms
    implement them differently.

    On Windows & Linux, a drag is a normal mouse move while a mouse button is
    held down. On OS X, a distinct "drag" event must be used instead.

    The code for moving and dragging the mouse is similar, so this function
    handles both. Users should call the moveTo() or dragTo() functions instead
    of calling _mouseMoveDrag().

    Args:
      moveOrDrag (str): Either 'move' or 'drag', for the type of action this is.
      x (int, float, None, optional): How far left (for negative values) or
        right (for positive values) to move the cursor. 0 by default.
      y (int, float, None, optional): How far up (for negative values) or
        down (for positive values) to move the cursor. 0 by default.
      xOffset (int, float, None, optional): How far left (for negative values) or
        right (for positive values) to move the cursor. 0 by default.
      yOffset (int, float, None, optional): How far up (for negative values) or
        down (for positive values) to move the cursor. 0 by default.
      duration (float, optional): The amount of time it takes to move the mouse
        cursor to the new xy coordinates. If 0, then the mouse cursor is moved
        instantaneously. 0.0 by default.
      tween (func, optional): The tweening function used if the duration is not
        0. A linear tween is used by default.
      button (str, int, optional): The mouse button released. TODO

    Returns:
      None
    """

    # The move and drag code is similar, but OS X requires a special drag event instead of just a move event when dragging.
    # See https://stackoverflow.com/a/2696107/1893164
    assert moveOrDrag in ("move", "drag"), "moveOrDrag must be in ('move', 'drag'), not %s" % (moveOrDrag)

    if sys.platform != "darwin":
        moveOrDrag = "move"  # Only OS X needs the drag event specifically.

    xOffset = int(xOffset) if xOffset is not None else 0
    yOffset = int(yOffset) if yOffset is not None else 0

    if x is None and y is None and xOffset == 0 and yOffset == 0:
        return  # Special case for no mouse movement at all.

    startx, starty = position()

    x = int(x) if x is not None else startx
    y = int(y) if y is not None else starty

    # x, y, xOffset, yOffset are now int.
    x += xOffset
    y += yOffset

    width, height = size()

    # Make sure x and y are within the screen bounds.
    # x = max(0, min(x, width - 1))
    # y = max(0, min(y, height - 1))

    # If the duration is small enough, just move the cursor there instantly.
    steps = [(x, y)]

    if duration > MINIMUM_DURATION:
        # Non-instant moving/dragging involves tweening:
        num_steps = max(width, height)
        sleep_amount = duration / num_steps
        if sleep_amount < MINIMUM_SLEEP:
            num_steps = int(duration / MINIMUM_SLEEP)
            sleep_amount = duration / num_steps

        steps = [getPointOnLine(startx, starty, x, y, tween(n / num_steps)) for n in range(num_steps)]
        # Making sure the last position is the actual destination.
        steps.append((x, y))

    for tweenX, tweenY in steps:
        if len(steps) > 1:
            # A single step does not require tweening.
            time.sleep(sleep_amount)

        tweenX = int(round(tweenX))
        tweenY = int(round(tweenY))

        # Moving the cursor to a fail-safe corner as part of the planned
        # mouse movements shouldn't trigger the fail-safe. This may seem
        # ridiculous, but remember that (tweenX, tweenY) is the *calculated*
        # coordinate of where the mouse should be, while failSafeCheck()
        # uses the *actual position* of the mouse from position() to
        # decide if it should raise the fail-safe exception.
        if (tweenX, tweenY) not in FAILSAFE_POINTS:
            failSafeCheck()

        if moveOrDrag == "move":
            platformModule._moveTo(tweenX, tweenY)
        elif moveOrDrag == "drag":
            platformModule._dragTo(tweenX, tweenY, button)
        else:
            raise NotImplementedError("Unknown value of moveOrDrag: {0}".format(moveOrDrag))

    if (tweenX, tweenY) not in FAILSAFE_POINTS:
        failSafeCheck()


# Keyboard Functions
# ==================


def isValidKey(key):
    """Returns a Boolean value if the given key is a valid value to pass to
    PyAutoGUI's keyboard-related functions for the current platform.

    This function is here because passing an invalid value to the PyAutoGUI
    keyboard functions currently is a no-op that does not raise an exception.

    Some keys are only valid on some platforms. For example, while 'esc' is
    valid for the Escape key on all platforms, 'browserback' is only used on
    Windows operating systems.

    Args:
      key (str): The key value.

    Returns:
      bool: True if key is a valid value, False if not.
    """
    return platformModule.keyboardMapping.get(key, None) != None


def keyDown(key, pause=None, logScreenshot=None, _pause=True):
    """Performs a keyboard key press without the release. This will put that
    key in a held down state.

    NOTE: For some reason, this does not seem to cause key repeats like would
    happen if a keyboard key was held down on a text field.

    Args:
      key (str): The key to be pressed down. The valid names are listed in
      KEYBOARD_KEYS.

    Returns:
      None
    """
    if len(key) > 1:
        key = key.lower()

    failSafeCheck()
    _logScreenshot(logScreenshot, "keyDown", key, folder=".")
    platformModule._keyDown(key)

    _autoPause(pause, _pause)


def keyUp(key, pause=None, logScreenshot=None, _pause=True):
    """Performs a keyboard key release (without the press down beforehand).

    Args:
      key (str): The key to be released up. The valid names are listed in
      KEYBOARD_KEYS.

    Returns:
      None
    """
    if len(key) > 1:
        key = key.lower()

    failSafeCheck()
    _logScreenshot(logScreenshot, "keyUp", key, folder=".")
    platformModule._keyUp(key)

    _autoPause(pause, _pause)


def press(keys, presses=1, interval=0.0, pause=None, logScreenshot=None, _pause=True):
    """Performs a keyboard key press down, followed by a release.

    Args:
      key (str, list): The key to be pressed. The valid names are listed in
      KEYBOARD_KEYS. Can also be a list of such strings.
      presses (integer, optiional): the number of press repetition
      1 by default, for just one press
      interval (float, optional): How many seconds between each press.
      0.0 by default, for no pause between presses.
      pause (float, optional): How many seconds in the end of function process.
      None by default, for no pause in the end of function process.
    Returns:
      None
    """
    if type(keys) == str:
        keys = [keys]  # If keys is 'enter', convert it to ['enter'].
    else:
        lowerKeys = []
        for s in keys:
            if len(s) > 1:
                lowerKeys.append(s.lower())
            else:
                lowerKeys.append(s)
    interval = float(interval)
    _logScreenshot(logScreenshot, "press", ",".join(keys), folder=".")
    for i in range(presses):
        for k in keys:
            failSafeCheck()
            platformModule._keyDown(k)
            platformModule._keyUp(k)
        time.sleep(interval)

    _autoPause(pause, _pause)


def typewrite(message, interval=0.0, pause=None, logScreenshot=None, _pause=True):
    """Performs a keyboard key press down, followed by a release, for each of
    the characters in message.

    The message argument can also be list of strings, in which case any valid
    keyboard name can be used.

    Since this performs a sequence of keyboard presses and does not hold down
    keys, it cannot be used to perform keyboard shortcuts. Use the hotkey()
    function for that.

    Args:
      message (str, list): If a string, then the characters to be pressed. If a
        list, then the key names of the keys to press in order. The valid names
        are listed in KEYBOARD_KEYS.
      interval (float, optional): The number of seconds in between each press.
        0.0 by default, for no pause in between presses.

    Returns:
      None
    """
    interval = float(interval)  # TODO - this should be taken out.

    failSafeCheck()

    _logScreenshot(logScreenshot, "write", message, folder=".")
    for c in message:
        if len(c) > 1:
            c = c.lower()
        press(c, _pause=False)
        time.sleep(interval)
        failSafeCheck()

    _autoPause(pause, _pause)


write = typewrite  # In PyAutoGUI 1.0, write() replaces typewrite().


def hotkey(*args, **kwargs):
    """Performs key down presses on the arguments passed in order, then performs
    key releases in reverse order.

    The effect is that calling hotkey('ctrl', 'shift', 'c') would perform a
    "Ctrl-Shift-C" hotkey/keyboard shortcut press.

    Args:
      key(s) (str): The series of keys to press, in order. This can also be a
        list of key strings to press.
      interval (float, optional): The number of seconds in between each press.
        0.0 by default, for no pause in between presses.

    Returns:
      None
    """
    interval = float(kwargs.get("interval", 0.0))  # TODO - this should be taken out.

    failSafeCheck()

    _logScreenshot(kwargs.get("logScreenshot"), "hotkey", ",".join(args), folder=".")
    for c in args:
        if len(c) > 1:
            c = c.lower()
        platformModule._keyDown(c)
        time.sleep(interval)
    for c in reversed(args):
        if len(c) > 1:
            c = c.lower()
        platformModule._keyUp(c)
        time.sleep(interval)

    _autoPause(kwargs.get("pause", None), kwargs.get("_pause", True))


def failSafeCheck():
    if FAILSAFE and tuple(position()) in FAILSAFE_POINTS:
        raise FailSafeException(
            "PyAutoGUI fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set pyautogui.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED."
        )


def displayMousePosition(xOffset=0, yOffset=0):
    """This function is meant to be run from the command line. It will
    automatically display the location and RGB of the mouse cursor."""
    try:
        runningIDLE = sys.stdin.__module__.startswith("idlelib")
    except:
        runningIDLE = False

    print("Press Ctrl-C to quit.")
    if xOffset != 0 or yOffset != 0:
        print("xOffset: %s yOffset: %s" % (xOffset, yOffset))
    try:
        while True:
            # Get and print the mouse coordinates.
            x, y = position()
            positionStr = "X: " + str(x - xOffset).rjust(4) + " Y: " + str(y - yOffset).rjust(4)
            if not onScreen(x - xOffset, y - yOffset) or sys.platform == "darwin":
                # Pixel color can only be found for the primary monitor, and also not on mac due to the screenshot having the mouse cursor in the way.
                pixelColor = ("NaN", "NaN", "NaN")
            else:
                pixelColor = pyscreeze.screenshot().getpixel(
                    (x, y)
                )  # NOTE: On Windows & Linux, getpixel() returns a 3-integer tuple, but on macOS it returns a 4-integer tuple.
            positionStr += " RGB: (" + str(pixelColor[0]).rjust(3)
            positionStr += ", " + str(pixelColor[1]).rjust(3)
            positionStr += ", " + str(pixelColor[2]).rjust(3) + ")"
            sys.stdout.write(positionStr)
            if not runningIDLE:
                # If this is a terminal, than we can erase the text by printing \b backspaces.
                sys.stdout.write("\b" * len(positionStr))
            else:
                # If this isn't a terminal (i.e. IDLE) then we can only append more text. Print a newline instead and pause a second (so we don't send too much output).
                sys.stdout.write("\n")
                time.sleep(1)
            sys.stdout.flush()
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        sys.stdout.flush()


def _snapshot(tag, folder=None, region=None, radius=None):
    # TODO feature not finished
    if region is not None and radius is not None:
        raise Exception("Either region or radius arguments (or neither) can be passed to snapshot, but not both")

    if radius is not None:
        x, y = platformModule._position()

    if folder is None:
        folder = os.getcwd()

    now = datetime.datetime.now()
    filename = "%s-%s-%s_%s-%s-%s-%s_%s.png" % (
        now.year,
        str(now.month).rjust(2, "0"),
        str(now.day).rjust(2, "0"),
        now.hour,
        now.minute,
        now.second,
        str(now.microsecond)[:3],
        tag,
    )
    filepath = os.path.join(folder, filename)
    screenshot(filepath)


def sleep(seconds):
    time.sleep(seconds)


def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(str(i), end=" ", flush=True)
        time.sleep(1)
    print()


def _getNumberToken(commandStr):
    """Gets the number token at the start of commandStr.

    Given '5hello' returns '5'
    Given '  5hello' returns '  5'
    Given '-42hello' returns '-42'
    Given '+42hello' returns '+42'
    Given '3.14hello' returns '3.14'

    Raises an exception if it can't tokenize a number.
    """
    pattern = re.compile(r"^(\s*(\+|\-)?\d+(\.\d+)?)")
    mo = pattern.search(commandStr)
    if mo is None:
        raise PyAutoGUIException("Invalid command at index 0: a number was expected")

    return mo.group(1)


def _getQuotedStringToken(commandStr):
    """Gets the quoted string token at the start of commandStr.
    The quoted string must use single quotes.

    Given "'hello'world" returns "'hello'"
    Given "  'hello'world" returns "  'hello'"

    Raises an exception if it can't tokenize a quoted string.
    """
    pattern = re.compile(r"^((\s*)('(.*?)'))")
    mo = pattern.search(commandStr)
    if mo is None:
        raise PyAutoGUIException("Invalid command at index 0: a quoted string was expected")

    return mo.group(1)


def _getParensCommandStrToken(commandStr):
    """Gets the command string token at the start of commandStr. It will also
    be enclosed with parentheses.

    Given "(ccc)world" returns "(ccc)"
    Given "  (ccc)world" returns "  (ccc)"
    Given "(ccf10(r))world" returns "(ccf10(r))"

    Raises an exception if it can't tokenize a quoted string.
    """

    # Check to make sure at least one open parenthesis exists:
    pattern = re.compile(r"^\s*\(")
    mo = pattern.search(commandStr)
    if mo is None:
        raise PyAutoGUIException("Invalid command at index 0: No open parenthesis found.")

    # Check to make sure the parentheses are balanced:
    i = 0
    openParensCount = 0
    while i < len(commandStr):
        if commandStr[i] == "(":
            openParensCount += 1
        elif commandStr[i] == ")":
            openParensCount -= 1
            if openParensCount == 0:
                i += 1  # Remember to increment i past the ) before breaking.
                break
            elif openParensCount == -1:
                raise PyAutoGUIException("Invalid command at index 0: No open parenthesis for this close parenthesis.")
        i += 1
    if openParensCount > 0:
        raise PyAutoGUIException("Invalid command at index 0: Not enough close parentheses.")

    return commandStr[0:i]


def _getCommaToken(commandStr):
    """Gets the comma token at the start of commandStr.

    Given ',' returns ','
    Given '  ,', returns '  ,'

    Raises an exception if a comma isn't found.
    """
    pattern = re.compile(r"^((\s*),)")
    mo = pattern.search(commandStr)
    if mo is None:
        raise PyAutoGUIException("Invalid command at index 0: a comma was expected")

    return mo.group(1)


def _tokenizeCommandStr(commandStr):
    """Tokenizes commandStr into a list of commands and their arguments for
    the run() function. Returns the list."""

    commandPattern = re.compile(r"^(su|sd|ss|c|l|m|r|g|d|k|w|h|f|s|a|p)")

    # Tokenize the command string.
    commandList = []
    i = 0  # Points to the current index in commandStr that is being tokenized.
    while i < len(commandStr):
        if commandStr[i] in (" ", "\t", "\n", "\r"):
            # Skip over whitespace:
            i += 1
            continue

        mo = commandPattern.match(commandStr[i:])
        if mo is None:
            raise PyAutoGUIException("Invalid command at index %s: %s is not a valid command" % (i, commandStr[i]))

        individualCommand = mo.group(1)
        commandList.append(individualCommand)
        i += len(individualCommand)

        # Handle the no argument commands (c, l, m, r, su, sd, ss):
        if individualCommand in ("c", "l", "m", "r", "su", "sd", "ss"):
            pass  # This just exists so these commands are covered by one of these cases.

        # Handle the arguments of the mouse (g)o and mouse (d)rag commands:
        elif individualCommand in ("g", "d"):
            try:
                x = _getNumberToken(commandStr[i:])
                i += len(x)  # Increment past the x number.

                comma = _getCommaToken(commandStr[i:])
                i += len(comma)  # Increment past the comma (and any whitespace).

                y = _getNumberToken(commandStr[i:])
                i += len(y)  # Increment past the y number.

            except PyAutoGUIException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                indexPart, colon, message = str(excObj).partition(":")

                indexNum = indexPart[len("Invalid command at index ") :]
                newIndexNum = int(indexNum) + i
                raise PyAutoGUIException("Invalid command at index %s:%s" % (newIndexNum, message))

            # Make sure either both x and y have +/- or neither of them do:
            if x.lstrip()[0].isdecimal() and not y.lstrip()[0].isdecimal():
                raise PyAutoGUIException("Invalid command at index %s: Y has a +/- but X does not." % (i - len(y)))
            if not x.lstrip()[0].isdecimal() and y.lstrip()[0].isdecimal():
                raise PyAutoGUIException(
                    "Invalid command at index %s: Y does not have a +/- but X does." % (i - len(y))
                )

            # Get rid of any whitespace at the front:
            commandList.append(x.lstrip())
            commandList.append(y.lstrip())

        # Handle the arguments of the (s)leep and (p)ause commands:
        elif individualCommand in ("s", "p"):
            try:
                num = _getNumberToken(commandStr[i:])
                i += len(num)  # Increment past the number.

                # TODO - raise an exception if a + or - is in the number.

            except PyAutoGUIException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                indexPart, colon, message = str(excObj).partition(":")

                indexNum = indexPart[len("Invalid command at index ") :]
                newIndexNum = int(indexNum) + i
                raise PyAutoGUIException("Invalid command at index %s:%s" % (newIndexNum, message))

            # Get rid of any whitespace at the front:
            commandList.append(num.lstrip())

        # Handle the arguments of the (k)ey press, (w)rite, (h)otkeys, and (a)lert commands:
        elif individualCommand in ("k", "w", "h", "a"):
            try:
                quotedString = _getQuotedStringToken(commandStr[i:])
                i += len(quotedString)  # Increment past the quoted string.
            except PyAutoGUIException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                indexPart, colon, message = str(excObj).partition(":")

                indexNum = indexPart[len("Invalid command at index ") :]
                newIndexNum = int(indexNum) + i
                raise PyAutoGUIException("Invalid command at index %s:%s" % (newIndexNum, message))

            # Get rid of any whitespace at the front and the quotes:
            commandList.append(quotedString[1:-1].lstrip())

        # Handle the arguments of the (f)or loop command:
        elif individualCommand == "f":
            try:
                numberOfLoops = _getNumberToken(commandStr[i:])
                i += len(numberOfLoops)  # Increment past the number of loops.

                subCommandStr = _getParensCommandStrToken(commandStr[i:])
                i += len(subCommandStr)  # Increment past the sub-command string.

            except PyAutoGUIException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                indexPart, colon, message = str(excObj).partition(":")

                indexNum = indexPart[len("Invalid command at index ") :]
                newIndexNum = int(indexNum) + i
                raise PyAutoGUIException("Invalid command at index %s:%s" % (newIndexNum, message))

            # Get rid of any whitespace at the front:
            commandList.append(numberOfLoops.lstrip())

            # Get rid of any whitespace at the front and the quotes:
            subCommandStr = subCommandStr.lstrip()[1:-1]
            # Recursively call this function and append the list it returns:
            commandList.append(_tokenizeCommandStr(subCommandStr))

    return commandList


def _runCommandList(commandList, _ssCount):
    i = 0
    while i < len(commandList):
        command = commandList[i]

        if command == "c":
            click(button=PRIMARY)
        elif command == "l":
            click(button=LEFT)
        elif command == "m":
            click(button=MIDDLE)
        elif command == "r":
            click(button=RIGHT)
        elif command == "su":
            scroll(1)  # scroll up
        elif command == "sd":
            scroll(-1)  # scroll down
        elif command == "ss":
            screenshot("screenshot%s.png" % (_ssCount[0]))
            _ssCount[0] += 1
        elif command == "s":
            sleep(float(commandList[i + 1]))
            i += 1
        elif command == "p":
            PAUSE = float(commandList[i + 1])
            i += 1
        elif command == "g":
            if commandList[i + 1][0] in ("+", "-") and commandList[i + 2][0] in ("+", "-"):
                move(int(commandList[i + 1]), int(commandList[i + 2]))
            else:
                moveTo(int(commandList[i + 1]), int(commandList[i + 2]))
            i += 2
        elif command == "d":
            if commandList[i + 1][0] in ("+", "-") and commandList[i + 2][0] in ("+", "-"):
                drag(int(commandList[i + 1]), int(commandList[i + 2]))
            else:
                dragTo(int(commandList[i + 1]), int(commandList[i + 2]))
            i += 2
        elif command == "k":
            press(commandList[i + 1])
            i += 1
        elif command == "w":
            write(commandList[i + 1])
            i += 1
        elif command == "h":
            hotkey(*commandList[i + 1].replace(" ", "").split(","))
            i += 1
        elif command == "a":
            alert(commandList[i + 1])
            i += 1
        elif command == "f":
            for j in range(int(commandList[i + 1])):
                _runCommandList(commandList[i + 2], _ssCount)
            i += 2
        i += 1


def run(commandStr, _ssCount=None):
    """Run a series of PyAutoGUI function calls according to a mini-language
    made for this function. The `commandStr` is composed of character
    commands that represent PyAutoGUI function calls.

    For example, `run('ccg-20,+0c')` clicks the mouse twice, then makes
    the mouse cursor go 20 pixels to the left, then click again.

    Whitespace between commands and arguments is ignored. Command characters
    must be lowercase. Quotes must be single quotes.

    For example, the previous call could also be written as `run('c c g -20, +0 c')`.

    The character commands and their equivalents are here:

    `c` => `click(button=PRIMARY)`
    `l` => `click(button=LEFT)`
    `m` => `click(button=MIDDLE)`
    `r` => `click(button=RIGHT)`
    `su` => `scroll(1) # scroll up`
    `sd` => `scroll(-1) # scroll down`
    `ss` => `screenshot('screenshot1.png') # filename number increases on its own`

    `gX,Y` => `moveTo(X, Y)`
    `g+X,-Y` => `move(X, Y) # The + or - prefix is the difference between move() and moveTo()`
    `dX,Y` => `dragTo(X, Y)`
    `d+X,-Y` => `drag(X, Y) # The + or - prefix is the difference between drag() and dragTo()`

    `k'key'` => `press('key')`
    `w'text'` => `write('text')`
    `h'key,key,key'` => `hotkey(*'key,key,key'.replace(' ', '').split(','))`
    `a'hello'` => `alert('hello')`

    `sN` => `sleep(N) # N can be an int or float`
    `pN` => `PAUSE = N # N can be an int or float`

    `fN(commands)` => for i in range(N): run(commands)

    Note that any changes to `PAUSE` with the `p` command will be undone when
    this function returns. The original `PAUSE` setting will be reset.

    TODO - This function is under development.
    """

    # run("ccc")  straight forward
    # run("susu") if 's' then peek at the next character
    global PAUSE

    if _ssCount is None:
        _ssCount = [
            0
        ]  # Setting this to a mutable list so that the callers can read the changed value. TODO improve this comment

    commandList = _tokenizeCommandStr(commandStr)

    # Carry out each command.
    originalPAUSE = PAUSE
    _runCommandList(commandList, _ssCount)
    PAUSE = originalPAUSE


# Add the bottom left, top right, and bottom right corners to FAILSAFE_POINTS.
_right, _bottom = size()
FAILSAFE_POINTS.extend([(0, _bottom - 1), (_right - 1, 0), (_right - 1, _bottom - 1)])
