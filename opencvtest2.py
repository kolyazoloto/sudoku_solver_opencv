#coding=utf-8
import cv2 as cv,numpy as np
import os,copy
####################################################################
#recognition code
def digit_recog(img):
    img = img
    img = cv.resize(img, (28, 19))
    mask = []
    result = []

    for ex_img in range(len(examples)):
        mask.append(copy.copy(img))
        one = 0
        nul = 0
        for i in range(len(examples[ex_img])):
            for j in range(len(examples[ex_img][i])):
                if (bool(img[i][j]) and bool(examples[ex_img][i][j])):
                    one += 1
                else:
                    nul += 1
        result.append([one+nul,nul])

    accur = 1
    digit = -1
    for index,i in enumerate(result):
        if (i[1]/i[0]) < accur:
            accur = i[1]/i[0]
            digit = index + 1
    return digit,accur


examples = []
current_folder = os.getcwd()
os.chdir(current_folder+"\data\examples")
# load examples
for index,i in enumerate(os.listdir()):
    if len(i) == 5:
        img = cv.imread(i,0)
        img = cv.resize(img,(28,19))
        img = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,3)
        examples.append(img)
        #cv.imshow(i,img)
os.chdir(current_folder)
# end load examples

############################# testing part  #########################
####################################################################
img = cv.imread("5.jpg",1)

img = cv.resize(img,None,fx=0.5, fy=0.5)

#canny = cv.Canny(img,100,200)
canny = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
canny = cv.adaptiveThreshold(canny, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 3)
contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

rot = 0
for index,cnt in enumerate(contours):
    if 180000< cv.contourArea(cnt) < 400000:
        #print(cv.contourArea(cnt))
        (x,y,w,h) = cv.boundingRect(contours[index])
        #print(w,h)
        if 200 < h < 700 and 200 < w < 700:
            #cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0),5)
            img_crop = img[y:y + h, x:x + w]
            rot = cv.minAreaRect(cnt)
            print (rot)
#########################################################################################
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
  return result
#img_crop = rotate_image(img_crop,3)
#canny_crop = cv.Canny(img_crop,100,300)
canny_crop = cv.cvtColor(img_crop, cv.COLOR_RGB2GRAY)
canny_crop = cv.adaptiveThreshold(canny_crop, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11,7)
contours, hierarchy = cv.findContours(canny_crop, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
os.chdir(os.getcwd()+'\data')
## Находим ячейки причем без повторов
prev = [[0,0,0,0]]
prev_digits = [[0,0,0,0]]


for index,cnt in enumerate(contours):

    if 1<cv.contourArea(cnt) < 6000:
        (x, y, w, h) = cv.boundingRect(cnt)
        if (20 < h < 55 and 10 < w < 40):
            isok = True
            #cv.rectangle(img_crop, (x, y), (x + w, y + h), (0, 0, 255), 4)
            for digit_i in prev_digits:
                if (abs(x - digit_i[0]) > 10 or abs(y - digit_i[1]) > 10):
                    continue
                else:
                    isok = False
                    break
            if (isok):
                prev_digits.append([x,y,w,h])
        if (40<h<100 and 40<w<100):
            isok = True
            #cv.rectangle(img_crop, (x, y), (x + w, y + h), (0, 255, 0),2)
            for prev_i in prev:
                if (abs(x - prev_i[0]) > 10 or abs(y - prev_i[1]) > 10):
                    continue
                else:
                    isok = False
                    break
            if (isok):
                prev.append([x,y,w,h])
#################################################################

def sort_key(x):
    return ((x[0]/60) + (x[1]/60)*9)


cells = prev[1:]
digits = prev_digits[1:]
sudoku_digits = []
count = 0
cells.sort(key=sort_key)
digits.sort(key=sort_key)

sudoku_list = [[0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0]]


for index_c,cell in enumerate(cells):
    x_c = cell[0]
    y_c = cell[1]
    w_c = cell[2]
    h_c = cell[3]
    for index_d,digit in enumerate(digits):
        x_d = digit[0]
        y_d = digit[1]
        w_d = digit[2]
        h_d = digit[3]
        if x_c < x_d < x_c + w_c and y_c < y_d < y_c + h_c:
            digit_img = img_crop[y_d:y_d + h_d, x_d:x_d + w_d]
            digit_img = cv.cvtColor(digit_img, cv.COLOR_RGB2GRAY)
            digit_img = cv.adaptiveThreshold(digit_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 1)
            result, accur = digit_recog(digit_img)
            sudoku_list[index_c // 9][index_c % 9] = result
##### solve sudoku
print(np.matrix(sudoku_list))
grid = sudoku_list
def possible(y,x,n):
    for i in range(0,9):
        if grid[y][i] == n:
            return False
    for i in range(0,9):
        if grid[i][x] == n:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j] == n:
                return False
    return True

def solve():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:
                for n in range(1,10):
                    if possible(y,x,n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    for index_c, cell in enumerate(cells):
        x_c = cell[0]
        y_c = cell[1]
        result = grid[index_c // 9][index_c % 9]
        #cv.rectangle(img_crop, (x_c, y_c), (x_c + w_c, y_c + h_c), (255, 255, 0),-1)
        cv.putText(img_crop, str(result), (x_c + 15 , y_c+35), cv.FONT_HERSHEY_TRIPLEX, 1.4, (50, 50, 200), 3)

solve()

cv.imshow("Sudoku window",img_crop)
cv.waitKey(0)