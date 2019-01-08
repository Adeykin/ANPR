import SquaredDetect
import sys, os
import cv2
import numpy as np


# 50x253
def dumpRects(img, rects, path):
    if not path:
        return
        
    for rect in rects:
        print 'dump rect: ' + str(rect)
        srcTri = np.float32([rect[0], rect[1], rect[3]])
        dstTri = np.float32([(0, 0), (253, 0), (0, 50) ])
        print 'srcTri: ' + str(srcTri)
        print 'dstTri: ' + str(dstTri)
        warpMat = cv2.getAffineTransform( srcTri, dstTri );
        warped = cv2.warpAffine( img, warpMat, (253,50) );
        cv2.imshow('warp', warped)
        cv2.waitKey()

        
    

def process(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY);
    
    detector = SquaredDetect.Detector()
    rects = detector.detect(gray)
    
    for a in rects:
        print a
        cv2.polylines(img, rects, True, (0,0,255))
    
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
        if vidcap: #video
            success,image = vidcap.read()
            while success:
                process(image)
                success,image = vidcap.read()
        else:      #image
            img = cv2.imread(path)    
            process(img)
    elif os.path.isdir(path): #directory
        for f in os.listdir(path):
            print 'try to read: ' + f
            img = cv2.imread(path + '/' + f)  
            rects = process(img)
            dumpRects(img, rects, outputPath)

