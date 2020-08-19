import zxing
import cv2
import operator
import os
import zxing
import sys
import numpy as np
import argparse
import imutils
from imutils.perspective import four_point_transform


def red(im):
    reader = zxing.BarCodeReader(java='java')
    barcode = reader.decode(im, try_harder=True)  # ,possible_formats ='ITF')#possible_formats ='ITF'
    print(barcode)
    return barcode


'''  
barcode = red('m/t4.jpg') #maxresdefault.jpg
d = barcode
if d:
   print(d.format)
   print(d.type)
   print(d.raw)
   print(d.parsed)
'''


def kmeans(input_img, k, i_val):
    hist = cv2.calcHist([input_img], [0], None, [256], [0, 256])
    img = input_img.ravel()
    img = np.reshape(img, (-1, 1))
    img = img.astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(img, k, None, criteria, 10, flags)
    centers = np.sort(centers, axis=0)

    return centers[i_val].astype(int), centers, hist


def cut(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # compute the Scharr gradient magnitude representation of the images
    # in both the x and y direction using OpenCV 2.4
    ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
    gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # blur and threshold the image
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)

    # find the contours in the thresholded image, then sort the contours
    # by their area, keeping only the largest one
    cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
    box = np.int0(box)
    warped = four_point_transform(image, box)
    return warped


def brightness(img):
    gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret3, thresh1 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)
    hist, bins = np.histogram(thresh1.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()

    pp = 100 * hist.max() / cdf.max()
    ppp = (int(pp) * 127 / 100)

    ret3, thresh1 = cv2.threshold(gray2, ppp, 255, cv2.THRESH_BINARY)
    kernelv = np.ones((1, 1), np.uint8)
    plateC = cv2.erode(thresh1, kernelv, iterations=1)
    ret3, op0 = cv2.threshold(plateC, ppp, 255, cv2.THRESH_BINARY)
    op = cv2.dilate(op0.copy(), kernelv, iterations=1)
    return op0


def thrrr(b, img):
    gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    ret, th1 = cv2.threshold(gray.copy(), 127, 255, cv2.THRESH_BINARY)

    cv2.imwrite('th.jpg', th1)
    b = red('th.jpg')
    if b is not None:
        return b
    elif b is None:
        # ret,th1 = cv2.threshold(gray.copy(),127,255,cv2.THRESH_BINARY)
        (thresh, th1) = cv2.threshold(gray.copy(), 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cv2.imwrite('th.jpg', th1)
        b = red('th.jpg')
        if b is not None:
            return b
        elif b is None:
            ret, th80 = cv2.threshold(gray.copy(), 25, 255, cv2.THRESH_BINARY)
            cv2.imwrite('th.jpg', th80)
            b = red('th.jpg')
            if b is not None:
                return b
            elif b is None:
                ret, th80 = cv2.threshold(gray.copy(), 15, 255, cv2.THRESH_BINARY)
                cv2.imwrite('th.jpg', th80)
                b = red('th.jpg')
                if b is not None:
                    return b

                elif b is None:
                    th2 = cv2.adaptiveThreshold(gray.copy(), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
                    cv2.imwrite('th2.jpg', th2)
                    b = red('th.jpg')
                    if b is not None:
                        return b
                    elif b is None:
                        th3 = cv2.adaptiveThreshold(gray.copy(), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                                    11, 2)
                        cv2.imwrite('th.jpg', th3)
                        b = red('th.jpg')
                        if b is not None:
                            return b
                        elif b is None:
                            ret, th4 = cv2.threshold(gray.copy(), 90, 255, cv2.THRESH_BINARY)
                            cv2.imwrite('th.jpg', th4)
                            b = red('th.jpg')
                            if b is not None:
                                return b
                            elif b is None:
                                blur = cv2.GaussianBlur(gray.copy(), (5, 5), 0)
                                ret3, th5 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                                cv2.imwrite('th.jpg', th5)
                                b = red('th.jpg')
                                if b is not None:
                                    return b
                                elif b is None:
                                    ret, th6 = cv2.threshold(gray.copy(), 127, 255, cv2.THRESH_BINARY)
                                    cv2.imwrite('thc.jpg', th6)
                                    b = red('thc.jpg')
                                    if b is not None:
                                        return b
                                    elif b is None:
                                        th8 = brightness(img)
                                        cv2.imwrite('th.jpg', th8)
                                        b = red('th.jpg')
                                        if b is not None:
                                            return b

                                        elif b is None:
                                            th22 = cv2.adaptiveThreshold(gray.copy(), 255,
                                                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                                         cv2.THRESH_BINARY, 115, 1)
                                            cv2.imwrite('th.jpg', th22)
                                            b = red('th.jpg')
                                            if b is not None:
                                                return b


def nor(b, img, im):
    cv2.imwrite('kmd.jpg', img)
    b = red('kmd.jpg')
    if b is not None:
        return b
    elif b is None:
        img = cv2.imread(im)
        kernel = np.ones((5, 5), np.float32) / 25
        dst = cv2.filter2D(img, -1, kernel)
        cv2.imwrite('00.jpg', dst)
        b = red('00.jpg')
        if b is not None:
            return b
        elif b is None:
            rows, cols, _ = img.shape

            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
            dst = cv2.warpAffine(img, M, (cols, rows))
            cv2.imwrite('00.jpg', dst)
            b = red('00.jpg')
            if b is not None:
                return b
            elif b is None:
                blur = cv2.bilateralFilter(img.copy(), 9, 75, 75)
                cv2.imwrite('00.jpg', blur)
                b = red('00.jpg')
                if b is not None:
                    return b
                elif b is None:
                    blur = cv2.GaussianBlur(img.copy(), (5, 5), 0)
                    cv2.imwrite('00.jpg', blur)
                    b = red('00.jpg')
                    if b is not None:
                        return b
                    elif b is None:
                        median = cv2.medianBlur(img.copy(), 5)
                        cv2.imwrite('00.jpg', median)
                        b = red('00.jpg')
                        if b is not None:
                            return b


def jm(img):
    gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dilated_img = cv2.dilate(gray2, np.ones((7, 7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(gray2, bg_img)
    norm_img = diff_img.copy()  # Needed for 3.x compatibility
    oop = cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    _, thr_img = cv2.threshold(norm_img, 230, 0, cv2.THRESH_TRUNC)
    op = cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    kernel = np.ones((2, 2), np.uint8)
    # dilation = cv2.dilate(op.copy(),kernel,iterations = 1)
    # ret3,op = cv2.threshold(op,99,255,cv2.THRESH_BINARY)
    return op


def fun_insanity(im):
    # ins = 0
    b = None
    img = cv2.imread(im)
    for ins in range(10):
        if ins == 0:
            b = nor(b, img, im)
            if b is not None:
                return b
            elif b is None:
                op = jm(img)
                cv2.imwrite('op.jpg', op)
                b = red('op.jpg')
                if b is not None:
                    return b
                elif b is None:
                    h, w, _ = img.shape
                    h2 = h / 4
                    w2 = w / 7

                    crop_img = img[int(h2):int(h - h2), int(w2):int(w - w2)]
                    b = nor(b, crop_img, im)
                    if b is not None:
                        return b

        elif b is None and ins == 1:  # gray
            img = cv2.imread(im)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('gray.jpg', gray)
            b = red('gray.jpg')
            if b is not None:
                return b

            elif b is None:
                equ = cv2.equalizeHist(gray.copy())
                res = np.hstack((gray.copy(), equ))  # stacking images side-by-side
                cv2.imwrite('res.jpg', res)
                b = red('res.jpg')
                if b is not None:
                    return b
                elif b is None:
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    cl1 = clahe.apply(gray.copy())

                    cv2.imwrite('res.jpg', cl1)
                    b = red('res.jpg')
                    if b is not None:
                        return b

        elif b is None and ins == 2:  # threshold all and all
            img = cv2.imread(im)
            b = thrrr(b, img)
            if b is not None:
                return b


        elif b is None and ins == 3:  # threshold  + morphological
            imgv = cv2.imread(im)
            gray = cv2.cvtColor(imgv.copy(), cv2.COLOR_BGR2GRAY)
            ret, th80 = cv2.threshold(gray.copy(), 80, 255, cv2.THRESH_BINARY)
            kernel = np.ones((2, 2), np.uint8)
            erosion = cv2.erode(th80.copy(), kernel, iterations=1)
            cv2.imwrite('thmor.jpg', erosion)
            b = red('thmor.jpg')
            if b is not None:
                return b
            elif b is None:
                dilation = cv2.dilate(th80.copy(), kernel, iterations=1)
                cv2.imwrite('thmor0.jpg', dilation)
                b = red('thmor0.jpg')
                if b is not None:
                    return b
                elif b is None:
                    opening = cv2.morphologyEx(th80.copy(), cv2.MORPH_OPEN, kernel)
                    cv2.imwrite('thmor.jpg', opening)
                    b = red('thmor.jpg')
                    if b is not None:
                        return b
                    elif b is None:
                        closing = cv2.morphologyEx(th80.copy(), cv2.MORPH_CLOSE, kernel)
                        cv2.imwrite('thmor.jpg', closing)
                        b = red('thmor.jpg')
                        if b is not None:
                            return b
                        elif b is None:
                            ret, th80 = cv2.threshold(gray.copy(), 99, 255, cv2.THRESH_BINARY)
                            kernel = np.ones((2, 2), np.uint8)
                            erosion = cv2.erode(th80.copy(), kernel, iterations=1)
                            cv2.imwrite('thmor.jpg', erosion)
                            b = red('thmor.jpg')
                            if b is not None:
                                return b
                            elif b is None:
                                ret, th80 = cv2.threshold(gray.copy(), 55, 255, cv2.THRESH_BINARY)
                                kernel = np.ones((3, 3), np.uint8)
                                dilation = cv2.dilate(th80.copy(), kernel, iterations=1)
                                cv2.imwrite('thmor0.jpg', dilation)
                                b = red('thmor0.jpg')
                                if b is not None:
                                    return b

        elif b is None and ins == 4:  # Derivatives gray
            gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
            laplacian = cv2.Laplacian(gray.copy(), cv2.CV_64F)
            cv2.imwrite('grlx.jpg', laplacian)
            b = red('grlx.jpg')
            if b is not None:
                return b
            elif b is None and ins == 40:
                sobelx = cv2.Sobel(gray.copy(), cv2.CV_64F, 1, 0, ksize=5)
                cv2.imwrite('grlx.jpg', sobelx)
                b = red('grlx.jpg')
                if b is not None:
                    return b
                elif b is None:
                    sobely = cv2.Sobel(gray.copy(), cv2.CV_64F, 0, 1, ksize=5)
                    cv2.imwrite('grlx.jpg', sobely)
                    b = red('grlx.jpg')
                    if b is not None:
                        return b
                    # elif b is None:


        elif b is None and ins == 6:
            wb = cut(img)
            # gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
            cv2.imwrite('cut.jpg', wb)
            b = red('cut.jpg')
            if b is not None:
                return b
            elif b is None:
                img = imutils.resize(img, width=600)
                wb = cut(img)
                cv2.imwrite('cut0.jpg', wb)
                b = red('cut0.jpg')
                if b is not None:
                    return b


        elif b is None and ins == 7:  # kmeans +threshold

            # _, thresh = cv2.threshold(img, kmeans(input_img=gray.copy(), k=8, i_val=2)[0], 255, cv2.THRESH_BINARY)

            # cv2.imwrite('thkm.jpg',thresh)
            # b = red('thkm.jpg')
            pass
            if b is not None:
                return b
            elif b is None:
                blur = cv2.GaussianBlur(gray.copy(), (5, 5), 0)
                ret3, th00 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                cv2.imwrite('thkm.jpg', th00)
                b = red('thkm.jpg')
                if b is not None:
                    return b

        elif b is None and ins == 9:
            return b


'''
imp = '../gpk.jpg' # '../imgg0.jpg'

pp = fun_insanity(imp) #'jk/maxresdefault.jpg')
imgdrow = cv2.imread(imp)
if pp:
   cv2.drawContours(imgdrow, [np.int0(pp.points)], -1, (0, 255, 0), 2)
   cv2.putText(imgdrow,str(pp.parsed),(50,50),cv2.FONT_HERSHEY_PLAIN, 2,(78,255,0),2)
   cv2.imwrite('imgdrow.jpg',imgdrow)
'''
