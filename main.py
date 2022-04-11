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
            return [[y1-1, x1-1], [y1, x1]]
    if(((x1-1)>=0) and ((y1+1)<=7)):
        if(matr[y1+1, x1-1] == matr[y1, x1]):
            return [[y1+1, x1-1], [y1, x1]]
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

template_names = ['blue', 'pink', 'green', 'yellow', 'violate', 'ice', 'chain']
template_chars = np.chararray((8, 8))
template_ice = np.chararray((8,8))
template_chained = np.chararray((8,8))

template_ice[:] = 'X'
template_chars[:] = 'X'
template_chained[:] = 'X'

isFirst = False
x1 = 0
y1 = 0

x2 = 0
y2 = 0

im = cv.imread('./examples/example.png')

plt.imshow(im)
plt.show()

size_of_block = ((im.shape[0]+im.shape[1])//2) // 8 #70
print(size_of_block)

for i, template_name in enumerate(template_names):
    img_rgb = im.copy()
    hsv = cv.cvtColor(img_rgb, cv.COLOR_BGR2HSV)
    coloured = np.zeros_like(img_rgb, np.uint8)

    if(template_name == 'green'):
        image_mask_green = cv.inRange(hsv, (33, 97, 32), (87, 255,255))
        image_imask = image_mask_green>0
    elif(template_name == 'violate'):
        image_mask_violate = cv.inRange(hsv, (125, 50, 141), (133, 180, 255))
        image_imask = image_mask_violate>0
    elif(template_name == 'yellow'):
        image_mask_yellow = cv.inRange(hsv, (0, 161, 0), (34, 255, 255))
        image_imask = image_mask_yellow>0
    elif(template_name == 'pink'):
        image_mask_pink = cv.inRange(hsv, (142,80,203), (179, 255, 255))
        image_imask = image_mask_pink>0
    elif((template_name == 'blue') or (template_name == 'ice')):
        image_mask_blue = cv.inRange(hsv, (92, 55, 104), (104, 255, 255))
        image_imask = image_mask_blue>0
    elif((template_name == 'chain')):
        image_mask_chain = cv.inRange(hsv, (0,0,0), (160, 76, 146))
        image_imask = image_mask_chain>0
    
    coloured[image_imask] = img_rgb[image_imask]
    img_coloured = cv.cvtColor(coloured, cv.COLOR_BGR2GRAY)

    plt.imshow(img_coloured)
    plt.show()
        
    template = cv.imread('./templates/' + template_name + '.png')
    template_hsv = cv.cvtColor(template, cv.COLOR_BGR2HSV)
    template_coloured = np.zeros_like(template, np.uint8)
        
    if(template_name == 'green'):
        template_mask_green = cv.inRange(template_hsv, (33, 97, 32), (87, 255,255))
        template_imask = template_mask_green>0
    elif(template_name == 'violate'):
        template_mask_violate = cv.inRange(template_hsv, (125, 50, 141), (133, 180, 255))
        template_imask = template_mask_violate>0
    elif(template_name == 'yellow'):
        template_mask_yellow = cv.inRange(template_hsv, (0, 161, 0), (34, 255, 255))
        template_imask = template_mask_yellow>0
    elif(template_name == 'pink'):
        template_mask_pink = cv.inRange(template_hsv, (142,80,203), (179, 255, 255))
        template_imask = template_mask_pink>0
    elif((template_name == 'blue') or (template_name == 'ice')):
        template_mask_blue = cv.inRange(template_hsv, (92, 55, 104), (104, 255, 255))
        template_imask = template_mask_blue>0
    elif((template_name == 'chain')):
        template_mask_chain = cv.inRange(template_hsv, (0,0,0), (160, 76, 146))
        template_imask = template_mask_chain>0
            
    template_coloured[template_imask] = template[template_imask]
    template_color = cv.cvtColor(template_coloured, cv.COLOR_BGR2GRAY)
        
    plt.imshow(template_color)
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
            
#make decision
decision = logic(template_chars, template_ice, template_chained)
#action
point1x = x1+((decision[0][1]*size_of_block)+(size_of_block//2))
point1y = y1+((decision[0][0]*size_of_block)+(size_of_block//2))
pyautogui.moveTo(point1x, point1y, duration=2, tween=pyautogui.easeInOutQuad)
point2x = x1+((decision[1][1]*size_of_block)+(size_of_block//2))
point2y = y1+((decision[1][0]*size_of_block)+(size_of_block//2))
pyautogui.moveTo(point2x, point2y, duration=2, tween=pyautogui.easeInOutQuad)

time.sleep(10)