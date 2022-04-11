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
            if(x!=7):     
                if(matr[y, x+1] == matr[y,x]):
                    check = find_horizontal_consequent(matr, y, x)
                    if((check != [-1,-1])
                       and (ice[check[0][0], check[0][1]] != 'i')
                       and (ice[check[1][0], check[1][1]] != 'i')
                       and (chain[check[0][0], check[0][1]] != 'c')
                       and (chain[check[1][0], check[1][1]] != 'c')):
                        return check
            if((x!=6) and (x!=7)):
                if(matr[y, x+2] == matr[y,x]):
                    check = find_horizontal_non_conseq(matr, y, x)
                    if((check != [-1,-1])
                       and (ice[check[0][0], check[0][1]] != 'i')
                       and (ice[check[1][0], check[1][1]] != 'i')
                       and (chain[check[0][0], check[0][1]] != 'c')
                       and (chain[check[1][0], check[1][1]] != 'c')):
                        return check
            #check vertical
            if(y!=7):
                if(matr[y+1, x] == matr[y,x]):
                    check = find_vertical_consequent(matr, y, x)
                    if((check != [-1,-1])
                       and (ice[check[0][0], check[0][1]] != 'i')
                       and (ice[check[1][0], check[1][1]] != 'i')
                       and (chain[check[0][0], check[0][1]] != 'c')
                       and (chain[check[1][0], check[1][1]] != 'c')):
                        return check
            if((y!=6) and (y!=7)):
                if(matr[y+2, x] == matr[y,x]):
                    check = find_vertical_non_conseq(matr, y, x)
                    if((check != [-1,-1])
                       and (ice[check[0][0], check[0][1]] != 'i')
                       and (ice[check[1][0], check[1][1]] != 'i')
                       and (chain[check[0][0], check[0][1]] != 'c')
                       and (chain[check[1][0], check[1][1]] != 'c')):
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

def detect(im, template_names, colored_templates_dict, filt_dict):   
    
    for i, template_name in enumerate(template_names):
        img_rgb = im.copy()
        
        template_color = colored_templates_dict[template_name]
        img_coloured = make_coloured(img_rgb, filt_dict[template_name][0], filt_dict[template_name][1])     
        
        plt.imshow(template_color)
        plt.show()
        
        plt.imshow(img_coloured)
        plt.show()
        
        res = cv.matchTemplate(img_coloured, template_color, cv.TM_CCOEFF_NORMED)#cv.TM_CCORR_NORMED 
        
        plt.imshow(res, cmap = 'gray')
        plt.colorbar();
        plt.show()
        
        threshold = 0.55#np.mean(res)+3*np.std(res)
        
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
        else:
            for pt in zip(*loc[::-1]):
                index_x = (pt[1]+(size_of_block//2)) // (size_of_block)
                index_y = (pt[0]+(size_of_block//2)) // (size_of_block)
                template_chars[index_x, index_y] = template_names[i][0]
    return template_chars, template_ice, template_chained

def action(decision):
    point1x = x1+((decision[0][1]*size_of_block)+(size_of_block//2))
    point1y = y1+((decision[0][0]*size_of_block)+(size_of_block//2))
    
    point2x = x1+((decision[1][1]*size_of_block)+(size_of_block//2))
    point2y = y1+((decision[1][0]*size_of_block)+(size_of_block//2))
    
    pyautogui.moveTo(point1x, point1y, duration=1, tween=pyautogui.easeInOutQuad)
    pyautogui.click(button='left')
    pyautogui.dragTo(point2x, point2y, 1, button='left')
    pyautogui.click(button='left')        
    time.sleep(3)

template_names = ['blue', 'pink', 'green', 'yellow', 'violate', 'ice', 'chain']

isFirst = False
x1 = 0
y1 = 0

x2 = 0
y2 = 0

#filters:
filt_dict = {'green':[(33, 97, 32), (87, 255,255)],
             'violate':[(125, 50, 141), (133, 180, 255)],
             'yellow':[(0, 161, 0), (34, 255, 255)],
             'pink':[(151,21,165), (179, 255, 255)],
             'blue':[(92, 55, 104), (104, 255, 255)],
             'ice':[(92, 55, 104), (104, 255, 255)],
             'chain':[(0,0,0),(160, 76, 146)]}

#templates_init
colored_templates_dict = templates_init(template_names, filt_dict)

#get_image
im = cv.imread('./examples/example5.png')

plt.imshow(im)
plt.show()

size_of_block = ((im.shape[0]+im.shape[1])//2) // 8
print(size_of_block)

#detect

template_chars = np.chararray((8, 8))
template_ice = np.chararray((8,8))
template_chained = np.chararray((8,8))

template_ice[:] = 'X'
template_chars[:] = 'X'
template_chained[:] = 'X'

chars, ice, chain = detect(im, template_names, colored_templates_dict, filt_dict)

#make decision
decision = logic(chars, ice, chain)
print(decision)

#make action
#action(decision)


            
#make decision
decision = logic(template_chars, template_ice, template_chained)
#action