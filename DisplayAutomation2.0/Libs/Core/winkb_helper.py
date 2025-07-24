###############################################################################
# @file         winkb_helper.py
# @brief        Helper module to simulate keyboard events
# @author       Beeresh, Vinod D S
###############################################################################

import time

import win32api
import win32con
from win32api import keybd_event

Base = {
    '0': 48,
    '1': 49,
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    '6': 54,
    '7': 55,
    '8': 56,
    '9': 57,
    'a': 65,
    'b': 66,
    'c': 67,
    'd': 68,
    'e': 69,
    'f': 70,
    'g': 71,
    'h': 72,
    'i': 73,
    'j': 74,
    'k': 75,
    'l': 76,
    'm': 77,
    'n': 78,
    'o': 79,
    'p': 80,
    'q': 81,
    'r': 82,
    's': 83,
    't': 84,
    'u': 85,
    'v': 86,
    'w': 87,
    'x': 88,
    'y': 89,
    'z': 90,
    'F1': 112,
    'F2': 113,
    'F3': 114,
    'F4': 115,
    'F5': 116,
    'F6': 117,
    'F7': 118,
    'F8': 119,
    'F9': 120,
    'F10': 121,
    'F11': 122,
    'F12': 123,
    '.': 190,
    '-': 189,
    ',': 188,
    '=': 187,
    '/': 191,
    ';': 186,
    '[': 219,
    ']': 221,
    '\\': 220,
    "'": 222,
    'ALT': 18,
    'TAB': 9,
    'CAPSLOCK': 20,
    'ENTER': 13,
    'BS': 8,
    'CTRL': 17,
    'ESC': 27,
    ' ': 32,
    'END': 35,
    'DOWN': 40,
    'LEFT': 37,
    'UP': 38,
    'RIGHT': 39,
    'SELECT': 41,
    'PRINTSCR': 44,
    'INS': 45,
    'DEL': 46,
    'LWIN': 91,
    'RWIN': 92,
    'LSHIFT': 160,
    'SHIFT': 161,
    'LCTRL': 162,
    'RCTRL': 163,
    'VOLUP': 175,
    'DOLDOWN': 174,
    'NUMLOCK': 144,
    'SCROLL': 145,
    'PAGEUP': 33,
    'PAGEDOWN': 34
}

Combs_2 = {
    'A': ['SHIFT', 'a'],
    'B': ['SHIFT', 'b'],
    'C': ['SHIFT', 'c'],
    'D': ['SHIFT', 'd'],
    'E': ['SHIFT', 'e'],
    'F': ['SHIFT', 'f'],
    'G': ['SHIFT', 'g'],
    'H': ['SHIFT', 'h'],
    'I': ['SHIFT', 'i'],
    'J': ['SHIFT', 'j'],
    'K': ['SHIFT', 'k'],
    'L': ['SHIFT', 'l'],
    'M': ['SHIFT', 'm'],
    'N': ['SHIFT', 'n'],
    'O': ['SHIFT', 'o'],
    'P': ['SHIFT', 'p'],
    'R': ['SHIFT', 'r'],
    'S': ['SHIFT', 's'],
    'T': ['SHIFT', 't'],
    'U': ['SHIFT', 'u'],
    'W': ['SHIFT', 'w'],
    'X': ['SHIFT', 'x'],
    'Y': ['SHIFT', 'y'],
    'Z': ['SHIFT', 'z'],
    'V': ['SHIFT', 'v'],
    'Q': ['SHIFT', 'q'],
    '?': ['SHIFT', '/'],
    '>': ['SHIFT', '.'],
    '<': ['SHIFT', ','],
    '"': ['SHIFT', "'"],
    ':': ['SHIFT', ';'],
    '|': ['SHIFT', '\\'],
    '}': ['SHIFT', ']'],
    '{': ['SHIFT', '['],
    '+': ['SHIFT', '='],
    '_': ['SHIFT', '-'],
    '!': ['SHIFT', '1'],
    '@': ['SHIFT', '2'],
    '#': ['SHIFT', '3'],
    '$': ['SHIFT', '4'],
    '%': ['SHIFT', '5'],
    '^': ['SHIFT', '6'],
    '&': ['SHIFT', '7'],
    '*': ['SHIFT', '8'],
    '(': ['SHIFT', '9'],
    ')': ['SHIFT', '0'],
    'ALT_ENTER': ['ALT', 'ENTER'],
    'WIN+A': ['LWIN', 'a'],
    'WIN+D': ['LWIN', 'd'],
    'WIN+E': ['LWIN', 'e'],
    'WIN+P': ['LWIN', 'p'],
    'WIN+C': ['LWIN', 'c'],
    'WIN+I': ['LWIN', 'i'],
    'WIN+T': ['LWIN', 't'],
    'ALT+TAB': ['ALT', 'TAB'],
    'WIN+M': ['LWIN', 'm'],
    'CTRL+T': ['CTRL', 't'],
    'CTRL+K': ['CTRL', 'k'],
    'CTRL+R': ['CTRL', 'r'],
    'WIN+RIGHT': ['LWIN', 'RIGHT'],
    'CTRL+C': ['CTRL', 'c'],
    'ALT+F4': ['ALT', 'F4'],
    'ALT+SPACE': ['ALT', " "],
    'CTRL+P': ['CTRL', 'p'],
    'SHIFT+TAB': ['SHIFT', 'TAB'],
    'ALT+L': ['ALT', 'l'],
    'SHIFT+RIGHT': ['SHIFT', 'RIGHT'],
    'SHIFT+LEFT': ['SHIFT', 'LEFT']
}

Combs_3 = {
    'SHIFT+WIN+M': ['SHIFT', 'LWIN', 'm'],
    'CTRL+ALT+DEL': ['CTRL', 'ALT', 'DEL']
}


##
# @brief        API to perform key up action
# @param[in]    Key - key combination
# @return       None
def key_up(Key):
    keybd_event(Key, 0, win32con.KEYEVENTF_KEYUP | win32con.KEYEVENTF_EXTENDEDKEY, 0)


##
# @brief        API to perform key down action
# @param[in]    Key - key combination
# @return       None
def key_down(Key):
    keybd_event(Key, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)


##
# @brief        API to perform key press action
# @param[in]    Key - key combination
# @param[in]    speed - speed of the key press
# @return       bool - True if key press is successful, None otherwise
def press(Key, speed=1):
    rest_time = 0.05 / speed
    if Key in Base:
        Key = Base[Key]
        key_down(Key)
        time.sleep(rest_time)
        key_up(Key)
        return True
    if Key in Combs_2:
        key_down(Base[Combs_2[Key][0]])
        time.sleep(rest_time)
        key_down(Base[Combs_2[Key][1]])
        time.sleep(rest_time)
        key_up(Base[Combs_2[Key][1]])
        time.sleep(rest_time)
        key_up(Base[Combs_2[Key][0]])
        return True
    if Key in Combs_3:
        key_down(Base[Combs_3[Key][0]])
        time.sleep(rest_time)
        key_down(Base[Combs_3[Key][1]])
        time.sleep(rest_time)
        key_down(Base[Combs_3[Key][2]])
        time.sleep(rest_time)
        key_up(Base[Combs_3[Key][2]])
        time.sleep(rest_time)
        key_up(Base[Combs_3[Key][1]])
        time.sleep(rest_time)
        key_up(Base[Combs_3[Key][0]])
        return True


##
# @brief        API to perform double click
# @param[in]    x - x coordinate of pointer location
# @param[in]    y - y coordinate of pointer location
# @return       None
def perform_double_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


##
# @brief        API to snap window to left
# @return       bool - True if action is completed successfully, False otherwise
def snap_left():
    rest_time = 0.05
    keys = ['LWIN', 'LEFT']
    key_down(Base[keys[0]])
    time.sleep(rest_time)
    key_down(Base[keys[1]])
    time.sleep(rest_time)
    key_up(Base[keys[1]])
    time.sleep(rest_time)
    key_up(Base[keys[0]])
    return True


##
# @brief        API to snap window to right
# @return       bool - True if action is completed successfully
def snap_right():
    rest_time = 0.05
    keys = ['LWIN', 'RIGHT']
    key_down(Base[keys[0]])
    time.sleep(rest_time)
    key_down(Base[keys[1]])
    time.sleep(rest_time)
    key_up(Base[keys[1]])
    time.sleep(rest_time)
    key_up(Base[keys[0]])
    return True
