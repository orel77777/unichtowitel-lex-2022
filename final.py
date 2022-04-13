import numpy as np
import cv2 as cv
from PIL import ImageGrab
import keyboard
import pyautogui
from matplotlib import pyplot as plt
import time

def find_horizontal_consequent(matr, y1, x1):
    if(((y1-1)>=0) and ((x1-1)>=0)):
        if(matr[y1-1, x1-1] == matr[y1, x1]):
            return [[y1-1, x1-1], [y1, x1-1]]
    if(((x1-1)>=0) and ((y1+1)<=7)):
        if(matr[y1+1, x1-1] == matr[y1, x1]):
            return [[y1+1, x1-1], [y1, x1-1]]
    if(((x1+2)<=7) and ((y1+1)<=7)):
        if(matr[y1+1, x1+2] == matr[y1, x1]):
            return [[y1+1, x1+2], [y1, x1+2]]
    if(((x1+2)<=7) and ((y1-1)>=0)):
        if(matr[y1-1, x1+2] == matr[y1, x1]):
            return [[y1-1, x1+2], [y1, x1+2]]
    return [-1,-1]

def find_horizontal_non_conseq(matr, y1, x1):
    if(((y1+1)<=7) and ((x1+1)<=7)):    
        if(matr[y1+1, x1+1] == matr[y1, x1]):
            return [[y1+1, x1+1], [y1, x1+1]]
    if(((y1-1)>=0) and ((x1+1)<=7)):
        if(matr[y1-1, x1+1] == matr[y1, x1]):
            return [[y1-1, x1+1], [y1, x1+1]]
    return [-1, -1]

def find_vertical_consequent(matr, y1, x1):
    if(((y1-1)>=0) and ((x1-1)>=0)):
        if(matr[y1-1, x1-1] == matr[y1, x1]):
            return [[y1-1, x1-1], [y1-1, x1]]
    if(((x1+1)<=0) and ((y1+2)<=7)):
        if(matr[y1+2, x1+1] == matr[y1, x1]):
            return [[y1+2, x1+1], [y1+2, x1]]
    if(((x1-1)>=0) and ((y1+2)<=7)):
        if(matr[y1+2, x1-1] == matr[y1, x1]):
            return [[y1+2, x1-1], [y1+2, x1]]
    if(((x1+1)<=7) and ((y1-1)>=0)):
        if(matr[y1-1, x1+1] == matr[y1, x1]):
            return [[y1-1, x1+1], [y1-1, x1]]
    return [-1,-1]

def find_vertical_non_conseq(matr, y1, x1):
    if(((y1+1)<=7) and ((x1+1)<=7)):
        if(matr[y1+1, x1+1] == matr[y1, x1]):
            return [[y1+1, x1+1], [y1+1, x1]]
    if(((y1+1)<=7) and ((x1-1)>=0)):
        if(matr[y1+1, x1-1] == matr[y1, x1]):
            return [[y1+1, x1-1], [y1+1, x1]]
    return [-1, -1]

def logic(matr, ice, chain):
    for y in [0,1,2,3,4,5,6,7]:
        for x in [0,1,2,3,4,5,6,7]:
            #check horizontal
            if((chain[y, x] != b'c') and (matr[y, x] != b'X')):
                if(x!=7):     
                    if((matr[y, x+1] == matr[y, x]) and (chain[y, x+1] != b'c')):
                        check = find_horizontal_consequent(matr, y, x)
                        if((check != [-1,-1])
                           and (ice[check[0][0], check[0][1]] != b'i')
                           and (ice[check[1][0], check[1][1]] != b'i')
                           and (chain[check[0][0], check[0][1]] != b'c')
                           and (chain[check[1][0], check[1][1]] != b'c')):
                            return check
                if((x!=6) and (x!=7)):
                     if((matr[y, x+2] == matr[y, x]) and (chain[y, x+2] != b'c')):
                        check = find_horizontal_non_conseq(matr, y, x)
                        if((check != [-1,-1])
                           and (ice[check[0][0], check[0][1]] != b'i')
                           and (ice[check[1][0], check[1][1]] != b'i')
                           and (chain[check[0][0], check[0][1]] != b'c')
                           and (chain[check[1][0], check[1][1]] != b'c')):
                            return check
                #check vertical
                if(y!=7):
                    if((matr[y+1, x] == matr[y, x]) and (chain[y+1, x] != b'c')):
                        check = find_vertical_consequent(matr, y, x)
                        if((check != [-1,-1])
                           and (ice[check[0][0], check[0][1]] != b'i')
                           and (ice[check[1][0], check[1][1]] != b'i')
                           and (chain[check[0][0], check[0][1]] != b'c')
                           and (chain[check[1][0], check[1][1]] != b'c')):
                            return check
                if((y!=6) and (y!=7)):
                    if((matr[y+2, x] == matr[y, x]) and (chain[y+2, x] != b'c')):
                        check = find_vertical_non_conseq(matr, y, x)
                        if((check != [-1,-1])
                           and (ice[check[0][0], check[0][1]] != b'i')
                           and (ice[check[1][0], check[1][1]] != b'i')
                           and (chain[check[0][0], check[0][1]] != b'c')
                           and (chain[check[1][0], check[1][1]] != b'c')):
                            return check         
    return 0

def make_coloured(picture, min_hsv, max_hsv):
    picture_hsv = cv.cvtColor(picture, cv.COLOR_BGR2HSV)
    picture_coloured = np.zeros_like(picture, np.uint8)    
    picture_mask = cv.inRange(picture_hsv, min_hsv, max_hsv)
    picture_imask = picture_mask>0
    picture_coloured[picture_imask] = picture[picture_imask]    
    picture_color = cv.cvtColor(picture_coloured, cv.COLOR_BGR2GRAY) 
    return picture_color


def templates_init(template_names, filt_dict):
    templates_dict = {}
    for template_name in template_names:
        template = cv.imread('./templates/' + template_name + '.png')
        templates_dict[template_name] = make_coloured(template, filt_dict[template_name][0], filt_dict[template_name][1])
    return templates_dict

def detect(im, template_names, colored_templates_dict, filt_dict, res_maps):   
    for i, template_name in enumerate(template_names):
        img_rgb = im.copy()
        
        template_color = colored_templates_dict[template_name]
        img_coloured = make_coloured(img_rgb, filt_dict[template_name][0], filt_dict[template_name][1])     
        
        res = cv.matchTemplate(img_coloured, template_color, cv.TM_CCOEFF_NORMED)#cv.TM_CCORR_NORMED 
        res_maps[template_name] = res
        
        if((template_name == 'chain') or (template_name == 'ice')):
            threshold = 0.4
        elif(template_name == 'blue'):
            threshold = 0.6
        else:
            threshold = 0.55
        
        loc = np.where(res >= threshold)
        
        if(template_name == 'ice'):
            for pt in zip(*loc[::-1]):
                index_x = (pt[1]+(size_of_block//2)) // (size_of_block)
                index_y = (pt[0]+(size_of_block//2)) // (size_of_block)
                template_ice[index_x, index_y] = 'i'
        elif(template_name == 'chain'):
            for pt in zip(*loc[::-1]):
                index_x = (pt[1]+(size_of_block//2)) // (size_of_block)
                index_y = (pt[0]+(size_of_block//2)) // (size_of_block)
                template_chained[index_x, index_y] = 'c'
        elif(template_name == 'blue_ice'):
            for pt in zip(*loc[::-1]):
                index_x = (pt[1]+(size_of_block//2)) // (size_of_block)
                index_y = (pt[0]+(size_of_block//2)) // (size_of_block)
                template_chars[index_x, index_y] = 'b'
                template_ice[index_x, index_y] = 'i'
        else:
            for pt in zip(*loc[::-1]):
                index_x = (pt[1]+(size_of_block//2)) // (size_of_block)
                index_y = (pt[0]+(size_of_block//2)) // (size_of_block)
                template_chars[index_x, index_y] = template_names[i][0]
    return template_chars, template_ice, template_chained

def action(decision, x1, y1):
    point1x = x1+((decision[0][1]*size_of_block)+(size_of_block//2))
    point1y = y1+((decision[0][0]*size_of_block)+(size_of_block//2))
    
    point2x = x1+((decision[1][1]*size_of_block)+(size_of_block//2))
    point2y = y1+((decision[1][0]*size_of_block)+(size_of_block//2))
    
    pyautogui.moveTo(point1x, point1y)
    pyautogui.click(button='left')
    pyautogui.dragTo(point2x, point2y, button='left')
    pyautogui.click(button='left')        
    time.sleep(3)

def repair(chars, res_maps):
    template_names = ['green', 'violet', 'yellow', 'pink', 'blue']
    maxes = np.zeros(len(template_names))
    for point in np.argwhere(chars == b'X'):
        y_i = point[0]*size_of_block
        x_i = point[1]*size_of_block
        y_e = y_i + (size_of_block // 10)
        x_e = x_i + (size_of_block // 10)
        for i, template_name in enumerate(template_names):
            maxes[i] = np.max(res_maps[template_name][y_i:y_e, x_i:x_e])
        if(np.max(maxes)>0):
            chars[point[0], point[1]] = template_names[np.argmax(maxes)][0]
    return 0

isFirst = False
x1 = 0
y1 = 0

x2 = 0
y2 = 0

#filters:
filt_dict = {'green':[(33, 97, 32), (87, 255,255)],
             'violet':[(125, 50, 141), (133, 180, 255)],
             'yellow':[(0, 161, 0), (34, 255, 255)],
             'pink':[(151, 21, 165), (179, 255, 255)],
             'blue':[(92, 55, 104), (104, 255, 255)],
             'yellow_ice':[(15, 109, 170), (31, 133, 198)],
             'green_ice':[(33, 97, 32), (87, 255,255)],
             'pink_ice':[(151,21,165), (179, 255, 255)],
             'blue_ice':[(92, 55, 104), (104, 255, 255)],
             'violet_ice':[(106, 41, 108), (134, 172, 255)],
             'ice':[(92, 55, 104), (104, 255, 255)],
             'chain':[(0, 0, 0),(132, 57, 107)]}

template_names = list(filt_dict.keys())

while True:
    if((keyboard.is_pressed('space')) and (isFirst == False)):
        mouse_x, mouse_y = pyautogui.position()
        x1 = mouse_x
        y1 = mouse_y
        print(x1, y1)
        isFirst = True
        keyboard.wait('alt')
    if((keyboard.is_pressed('space')) and (isFirst == True)):
        mouse_x, mouse_y = pyautogui.position()
        x2 = mouse_x
        y2 = mouse_y
        print(x2, y2)
        isFirst = False
        break

#templates_init
colored_templates_dict = templates_init(template_names, filt_dict)

img = ImageGrab.grab(bbox=(x1, y1, x2, y2))        
img_np = np.array(img)
im = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)
size_of_block = ((im.shape[0]+im.shape[1])//2) // 8

if((size_of_block)<70 or (size_of_block>80)):
    print('Too big image. Inconsistent of template size and image')
    exit(0)

while True:
    template_chars = np.chararray((8, 8))
    template_ice = np.chararray((8,8))
    template_chained = np.chararray((8,8))

    template_ice[:] = 'X'
    template_chars[:] = 'X'
    template_chained[:] = 'X'
    
    #detect
    res_maps = {}
    chars, ice, chain = detect(im, template_names, colored_templates_dict, filt_dict, res_maps)
    
    #repair
    if(np.isin('X', chars)):
        repair(chars, res_maps)
    print(chars)
    
    #make decision
    decision = logic(chars, ice, chain)
    print(decision)
    
    #make action
    action(decision, x1, y1)
    
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))        
    img_np = np.array(img)
    im = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)