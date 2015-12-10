__Author__ = 'Jesse Moy'

import re
import os
import pywinauto
import pyautogui
# import win32gui
# import time
# import fnmatch
# from osgeo import gdal
# from osgeo import gdal_array
# import logging
# import numpy
from pywinauto.application import Application
# import random
import arcpy
import logging

import ctypes
import win32gui
# EnumWindows = ctypes.windll.user32.EnumWindows
# EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
# GetWindowText = ctypes.windll.user32.GetWindowTextW
# GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
# IsWindowVisible = ctypes.windll.user32.IsWindowVisible
#
# titles = []
# def foreach_window(hwnd, lParam):
#     if IsWindowVisible(hwnd):
#         length = GetWindowTextLength(hwnd)
#         buff = ctypes.create_unicode_buffer(length + 1)
#         GetWindowText(hwnd, buff, length + 1)
#         titles.append((hwnd, buff.value))
#     return True
# EnumWindows(EnumWindowsProc(foreach_window), 0)
#
# for i in range(len(titles)):
#     print(titles)[i]