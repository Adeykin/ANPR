import SquaredDetect
import sys, os
import cv2

def process(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY);
    
    detector = SquaredDetect.Detector()
    rects = detector.detect(gray)
    
    for a in rects:
        print a
        cv2.polylines(img, rects, True, (0,0,255))
    
    cv2.imshow('img', img)
    cv2.waitKey()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'python demo.py <imageOrVideoPath>'
    path = sys.argv[1]
    print 'reading: ' + path
    
    if os.path.isfile(path):
        vidcap = cv2.VideoCapture(path)
        if vidcap:
            success,image = vidcap.read()
            while success:
                process(image)
                success,image = vidcap.read()
        else:
            img = cv2.imread(path)    
            process(img)
    elif os.path.isdir(path):
        for f in os.listdir(path):
            print 'try to read: ' + f
            img = cv2.imread(path + '/' + f)  
            process(img)

