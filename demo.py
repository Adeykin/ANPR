import SquaredDetect
import TesseractRecogniser
import Warper
import sys, os
import cv2
import numpy as np


# 50x253
def dumpRects(img, rects, path, imgName):
    if not path:
        return
    
    warper = Warper.Warper()
    
    for i, rect in enumerate(rects):
        warp = warper.warp(img, rect)
        #cv2.imshow('warp', warped)
        #cv2.waitKey()
        cv2.imwrite(path + '/' + str(i) + '_' + imgName, warp)


def process(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY);
    
    detector = SquaredDetect.Detector() #TODO: Use global objects
    recogniser = TesseractRecogniser.Recogniser()
    rects = detector.detect(gray)
    
    cv2.polylines(img, rects, True, (0,0,255))
    for rect in rects:
        text = recogniser.recognise(img, rect)
        print rect
        print('Recognised: ' + text)
        cv2.putText(img, text, tuple(rect[0]), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color=(0,0,255))
    
    cv2.imshow('img', img)
    cv2.waitKey()
    
    return rects


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'python demo.py <imageOrVideoPath>'
    path = sys.argv[1]
    print 'reading: ' + path
    
    outputPath = None
    if len(sys.argv) == 3:
        outputPath = sys.argv[2]
    
    if os.path.isfile(path):
        vidcap = cv2.VideoCapture(path)
        if vidcap:            #video
            success,image = vidcap.read()
            while success:
                process(image.copy())
                success,image = vidcap.read()
        else:                 #image
            img = cv2.imread(path)    
            process(img)
    elif os.path.isdir(path): #directory
        for f in os.listdir(path):
            print 'try to read: ' + f
            img = cv2.imread(path + '/' + f)  
            rects = process(img.copy())
            dumpRects(img, rects, outputPath, f)

