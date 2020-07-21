
import numpy as np,os
import cv2 as cv
import copy

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
        #print(i[1]/i[0])

    return digit,accur

current_folder = os.getcwd()
os.chdir(current_folder+"\examples")
# load examples
for index,i in enumerate(os.listdir()):
    if len(i) == 5:

        img = cv.imread(i,0)
        #print(img.shape)
        img = cv.resize(img,(28,19))
        img = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,3)
        examples.append(img)
        #cv.imshow(i,img)
os.chdir(current_folder)
# end load examples

img = cv.imread('9.jpg',0)
img = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,3)

digit,accur = digit_recog(img)
print(digit)

#cv.imshow("recog",img)



cv.waitKey(0)






