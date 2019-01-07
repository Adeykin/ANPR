import SquaredDetect
import sys
import cv2

if __name__ == '__main__':
    #if len(sys.argv) != 2:
    #print 'python demo.py <imageOrVideoPath>'
    path = sys.argv[1]
    #print('reading: ' + path)
    
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY);
    
    detector = SquaredDetect.Detector()
    rects = detector.detect(gray)
    
    for a in rects:
        print a
        cv2.polylines(img, rects, True, (0,0,255))
    
    
    cv2.imshow('img', img)
    cv2.waitKey()
