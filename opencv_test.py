#coding=utf-8
import cv2 as cv,numpy as np
import os,copy

####################################################################
#recognition code
examples = []

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
                #mask[ex_img][i][j] = bool(img[i][j]) and bool(examples[ex_img][i][j])
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
img = cv.imread("3.jpg",1)

img = cv.resize(img,None,fx=0.5, fy=0.5)

canny = cv.Canny(img,200,600)
contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
sudoku_contour = None
for index,cnt in enumerate(contours):
    if cv.contourArea(cnt) > 13000:
        #print(contours[index])
        (x,y,w,h) = sudoku_contour = cv.boundingRect(contours[index])
        sudoku_cnt = contours[index]
        #cv.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)

#########################################################################################
img_crop = img[y:y+h, x:x+w]
canny_crop = cv.Canny(img_crop,200,400)
contours, hierarchy = cv.findContours(canny_crop, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

os.chdir(os.getcwd()+'\data')
count = 0
prev = [0,0,0,0]
sudoku_digits = []
for index,cnt in enumerate(contours):
    if 1<cv.contourArea(cnt) < 4000:
        (x,y,w,h) = cv.boundingRect(contours[index])
        if (15<h<40):
            count += 1
            digit_img = img_crop[y:y + h, x:x + w]
            digit_img = cv.cvtColor(digit_img, cv.COLOR_RGB2GRAY)
            digit_img = cv.adaptiveThreshold(digit_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 3)
            digit, accur = digit_recog(digit_img)
            if (abs(x - prev[0]) > 10 or abs(y - prev[1]) > 10):
                sudoku_digits.append([digit,[x,y,w,h]])
        prev = [x,y,w,h]
'''for i in sudoku_digits:
    x = i[1][0]
    y = i[1][1]
    w = i[1][2]
    h = i[1][3]
    cv.rectangle(img_crop, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #cv.putText(img_crop,str(i[0]),(x,y),font,0.9,(255,0,0),2,cv.LINE_AA)
    cv.imshow("Sudoku img",img_crop)
    print(i[0])
print(len(sudoku_digits))'''


sudoku_list = [[0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0]]

x_sred = np.ceil(sudoku_contour[2]/9)
y_sred = np.ceil(sudoku_contour[3]/9)

for index in range(len(sudoku_digits)):
    x = sudoku_digits[index][1][0]
    y = sudoku_digits[index][1][1]

    sudoku_list[int(y/y_sred)][int(x/x_sred)] = sudoku_digits[index][0]


# Надо как то отсортировать
print(sudoku_list)

cv.imshow("Sudoku window",img_crop)

cv.waitKey(0)