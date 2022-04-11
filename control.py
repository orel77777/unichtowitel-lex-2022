#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 23:08:28 2022

@author: ivan
"""

import numpy as np
import cv2 as cv
from PIL import ImageGrab
import keyboard
import pyautogui

pyautogui.moveTo(300, 300, 2, pyautogui.easeInQuad)
pyautogui.click(button='left')
pyautogui.dragTo(500, 500, 2, button='left')
pyautogui.click(button='left')


# isFirst = False
# x1 = 0
# y1 = 0

# x2 = 0
# y2 = 0

# while True:
#     if((keyboard.is_pressed('space')) and (isFirst == False)):
#         mouse_x, mouse_y = pyautogui.position()
#         x1 = mouse_x
#         y1 = mouse_y
#         print(x1, y1)
#         isFirst = True
#         keyboard.wait('alt')
#     if((keyboard.is_pressed('space')) and (isFirst == True)):
#         mouse_x, mouse_y = pyautogui.position()
#         x2 = mouse_x
#         y2 = mouse_y
#         print(x2, y2)
#         img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
#         isFirst = False
#         img_np = np.array(img)
#         frame = cv.cvtColor(img_np, cv.COLOR_BGR2GRAY)
#         cv.imshow("frame", frame)
#         break 

# cv.waitKey(0)
# cv.destroyAllWindows()

# while True:
#     img = ImageGrab.grab(bbox=(0, 1000, 100, 1100)) #x, y, w, h
#     img_np = np.array(img)
#     frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
#     cv2.imshow("frame", frame)
#     if cv2.waitKey(1) & 0Xff == ord('q'):
#         break

##q - quit

# img = cv.imread('res.png')
# cv.imshow('image', img)
#define the events for the
# mouse_click.

        
# img_np = np.array(img)
# frame = cv.cvtColor(img_np, cv.COLOR_BGR2GRAY)
