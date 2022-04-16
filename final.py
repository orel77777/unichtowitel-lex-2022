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
    if(((x1-1)>=0) and ((y1+1)<=(matr.shape[0]-1))):
        if(matr[y1+1, x1-1] == matr[y1, x1]):
            return [[y1+1, x1-1], [y1, x1-1]]
    if(((x1+2)<=(matr.shape[1]-1)) and ((y1+1)<=(matr.shape[0]-1))):
        if(matr[y1+1, x1+2] == matr[y1, x1]):
            return [[y1+1, x1+2], [y1, x1+2]]
    if(((x1+2)<=(matr.shape[1]-1)) and ((y1-1)>=0)):
        if(matr[y1-1, x1+2] == matr[y1, x1]):
            return [[y1-1, x1+2], [y1, x1+2]]
    if((x1-2)>=0):    
        if(matr[y1, x1-2] == matr[y1, x1]):
            return [[y1, x1-2], [y1, x1-1]]
    if((x1+3)<=(matr.shape[1]-1)):    
        if(matr[y1, x1+3] == matr[y1, x1]):
            return [[y1, x1+3], [y1, x1+2]]
    return [-1,-1]

def find_horizontal_non_conseq(matr, y1, x1):
    if(((y1+1)<=(matr.shape[0]-1)) and ((x1+1)<=(matr.shape[1]-1))):    
        if(matr[y1+1, x1+1] == matr[y1, x1]):
            return [[y1+1, x1+1], [y1, x1+1]]
    if(((y1-1)>=0) and ((x1+1)<=(matr.shape[1]-1))):
        if(matr[y1-1, x1+1] == matr[y1, x1]):
            return [[y1-1, x1+1], [y1, x1+1]]
    return [-1, -1]

def find_vertical_consequent(matr, y1, x1):
    if(((y1-1)>=0) and ((x1-1)>=0)):
        if(matr[y1-1, x1-1] == matr[y1, x1]):
            return [[y1-1, x1-1], [y1-1, x1]]
    if(((x1+1)<=(matr.shape[1]-1)) and ((y1+2)<=(matr.shape[0]-1))):
        if(matr[y1+2, x1+1] == matr[y1, x1]):
            return [[y1+2, x1+1], [y1+2, x1]]
    if(((x1-1)>=0) and ((y1+2)<=(matr.shape[0]-1))):
        if(matr[y1+2, x1-1] == matr[y1, x1]):
            return [[y1+2, x1-1], [y1+2, x1]]
    if(((x1+1)<=(matr.shape[1]-1)) and ((y1-1)>=0)):
        if(matr[y1-1, x1+1] == matr[y1, x1]):
            return [[y1-1, x1+1], [y1-1, x1]]
    if((y1-2)>=0):    
        if(matr[y1-2, x1] == matr[y1, x1]):
            return [[y1-2, x1], [y1-1, x1]]
    if((y1+3)<=(matr.shape[0]-1)):    
        if(matr[y1+3, x1] == matr[y1, x1]):
            return [[y1+3, x1], [y1+2, x1]]
    return [-1,-1]

def find_vertical_non_conseq(matr, y1, x1):
    if(((y1+1)<=7) and ((x1+1)<=7)):
        if(matr[y1+1, x1+1] == matr[y1, x1]):
            return [[y1+1, x1+1], [y1+1, x1]]
    if(((y1+1)<=7) and ((x1-1)>=0)):
        if(matr[y1+1, x1-1] == matr[y1, x1]):
            return [[y1+1, x1-1], [y1+1, x1]]
    return [-1, -1]

def logic(matr, ice_chain, not_movable_chars, fixed_chars, unrec_char):
    for y in np.arange(matr.shape[0]):
        for x in np.arange(matr.shape[1]):
            if((not (ice_chain[y, x] in fixed_chars)) and (matr[y, x] != unrec_char)):
                #check horizontal
                if(x != matr.shape[1] - 1):
                    if((matr[y, x+1] == matr[y, x]) and (not (ice_chain[y, x+1] in fixed_chars))):
                        check = find_horizontal_consequent(matr, y, x)
                        if((check != [-1,-1]) and (not (ice_chain[check[0][0], check[0][1]] in not_movable_chars)) and (not (ice_chain[check[1][0], check[1][1]] in not_movable_chars))):
                            return check
                if((x != matr.shape[1] - 2) and (x != matr.shape[1] - 1)):
                     if((matr[y, x+2] == matr[y, x]) and (not (ice_chain[y, x+2] in fixed_chars))):
                        check = find_horizontal_non_conseq(matr, y, x)
                        if((check != [-1,-1]) and (not (ice_chain[check[0][0], check[0][1]] in not_movable_chars)) and (not (ice_chain[check[1][0], check[1][1]] in not_movable_chars))):
                            return check
                #check vertical
                if(y != matr.shape[0] - 1):
                    if((matr[y+1, x] == matr[y, x]) and (not (ice_chain[y+1, x] in fixed_chars))):
                        check = find_vertical_consequent(matr, y, x)
                        if((check != [-1,-1]) and (not (ice_chain[check[0][0], check[0][1]] in not_movable_chars)) and (not (ice_chain[check[1][0], check[1][1]] in not_movable_chars))):
                            return check
                if((y != matr.shape[0] - 2) and (y != matr.shape[0] - 1)):
                    if((matr[y+2, x] == matr[y, x]) and (not (ice_chain[y+2, x] in fixed_chars))):
                        check = find_vertical_non_conseq(matr, y, x)
                        if((check != [-1,-1]) and (not (ice_chain[check[0][0], check[0][1]] in not_movable_chars)) and (not (ice_chain[check[1][0], check[1][1]] in not_movable_chars))):
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

def detect(im, size_of_block,
                           template_chars, template_specific_blocks,
                           template_names, specific_template_names,
                           colored_templates_dict, filt_dict,
                           res_maps, main_threshold, specific_types_threshold):   

    for i, template_name in enumerate(template_names):
        img_rgb = im.copy()
        
        template_color = colored_templates_dict[template_name]
        img_coloured = make_coloured(img_rgb, filt_dict[template_name][0], filt_dict[template_name][1])     
        
        res = cv.matchTemplate(img_coloured, template_color, cv.TM_CCOEFF_NORMED)
        res_maps[template_name] = res
        
        if(template_name in specific_template_names):
            threshold = specific_types_threshold
        elif(template_name == 'blue'):
            threshold = main_threshold+0.05
        else:
            threshold = main_threshold
        
        loc = np.where(res >= threshold)
        
        if(template_name in specific_template_names):
            for pt in zip(*loc[::-1]):
                index_x = (pt[1]+(size_of_block//2)) // (size_of_block)
                index_y = (pt[0]+(size_of_block//2)) // (size_of_block)
                template_specific_blocks[index_x, index_y] = template_names[i][0]
        elif(template_name == 'blue_ice'):
            for pt in zip(*loc[::-1]):
                index_x = (pt[1]+(size_of_block//2)) // (size_of_block)
                index_y = (pt[0]+(size_of_block//2)) // (size_of_block)
                template_chars[index_x, index_y] = 'b'
                template_specific_blocks[index_x, index_y] = 'i'
        else:
            for pt in zip(*loc[::-1]):
                index_x = (pt[1]+(size_of_block//2)) // (size_of_block)
                index_y = (pt[0]+(size_of_block//2)) // (size_of_block)
                template_chars[index_x, index_y] = template_names[i][0]
    return template_chars, template_specific_blocks

def action(decision, x1, y1, size_of_block):
    if(decision != 0):    
        point1x = x1+((decision[0][1]*size_of_block)+(size_of_block//2))
        point1y = y1+((decision[0][0]*size_of_block)+(size_of_block//2))
        
        point2x = x1+((decision[1][1]*size_of_block)+(size_of_block//2))
        point2y = y1+((decision[1][0]*size_of_block)+(size_of_block//2))
        
        pyautogui.moveTo(point1x, point1y)
        pyautogui.click(button='left')
        pyautogui.dragTo(point2x, point2y, button='left')
        pyautogui.click(button='left')
        pyautogui.click(button='left')
    time.sleep(4)

def repair(size_of_block, main_template_names, chars, unrec_chars,
       res_maps, repair_individual_threshold):
    template_names = main_template_names
    maxes = np.zeros(len(template_names))
    for point in np.argwhere(chars == unrec_char):
        y_i = point[0]*size_of_block
        x_i = point[1]*size_of_block
        y_e = y_i + (size_of_block // 10)
        x_e = x_i + (size_of_block // 10)
        for i, template_name in enumerate(template_names):
            maxes[i] = np.max(res_maps[template_name][y_i:y_e, x_i:x_e])
        if(np.max(maxes) > repair_individual_threshold):
            chars[point[0], point[1]] = template_names[np.argmax(maxes)][0]
    return 0

def get_image_by_screen(x1, y1, x2, y2):
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))        
    img_np = np.array(img)
    im = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)
    return im
    
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
             'yellow_ice':[(8, 52, 154), (34, 133, 203)],
             'green_ice':[(33, 97, 32), (87, 255,255)],
             'pink_ice':[(151,21,165), (179, 255, 255)],
             'blue_ice':[(92, 55, 104), (104, 255, 255)],
             'violet_ice':[(106, 41, 108), (134, 172, 255)],
             'ice':[(92, 55, 104), (104, 255, 255)],
             'chain':[(0, 0, 0),(132, 57, 107)]}

template_names = list(filt_dict.keys())
main_template_names = ['green', 'violet', 'yellow', 'pink', 'blue']
specific_template_names = ['ice', 'chain']

not_movable_chars = np.array([x[0] for x in specific_template_names], dtype='|S1')
fixed_chars = [b'c']
unrec_char = b'X'

repair_individual_threshold = 0.1
specific_types_threshold = 0.4
main_threshold = 0.55

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

#get_first_image
im = get_image_by_screen(x1, y1, x2, y2)
size_of_block = ((im.shape[0]+im.shape[1])//2) // 8

if((size_of_block)<70 or (size_of_block>80)):
    print('Too big image. Inconsistent of template size and image')
    exit(0)

while True:
    template_chars = np.chararray((8, 8))
    template_specific_blocks = np.chararray((8,8))
    
    template_specific_blocks[:] = unrec_char
    template_chars[:] = unrec_char
    
    #detect
    res_maps = {}
    chars, ice_chain = detect(im, size_of_block,
                               template_chars, template_specific_blocks,
                               template_names, specific_template_names,
                               colored_templates_dict, filt_dict,
                               res_maps, main_threshold, specific_types_threshold)
    
    #repair
    if(np.isin(unrec_char, chars)):
        repair(size_of_block, main_template_names, chars, unrec_char,
               res_maps, repair_individual_threshold)
    print(chars)
    
    #make decision
    decision = logic(chars, ice_chain, not_movable_chars, fixed_chars, unrec_char)
    print(decision)
    
    #make action
    action(decision, x1, y1, size_of_block)
    
    #get_image
    im = get_image_by_screen(x1, y1, x2, y2)