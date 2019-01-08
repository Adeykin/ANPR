import cv2
import numpy as np

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )
    
def distance(p0, p1):
    return np.sqrt( (p0[0]-p1[0])**2 + (p0[1]-p1[1])**2)
    
class Detector:
    def __init__(self):
        self.maxCos = 0.2
        self.minArea = 100
        self.relation = 0.197628458
        self.relationEpsilon = 0.04
        
    def checkProportions(self, rect):
        lenghts = [ distance(rect[i%4], rect[(i+1)%4]) for i in range(4)]
        lenghts.sort()
        print 'relation: ' + str(lenghts[0]/lenghts[3])
        return np.abs(lenghts[0]/lenghts[3] - self.relation) < self.relationEpsilon       

    def find_squares(self, img):
        img = cv2.GaussianBlur(img, (5, 5), 0)
        squares = []
        for gray in cv2.split(img):
            for thrs in range(0, 255, 26):
                if thrs == 0:
                    bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                    bin = cv2.dilate(bin, None)
                else:
                    retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
                tuple = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                #print len(tuple)
                bin, contours, hierarchy = tuple
                for cnt in contours:
                    cnt_len = cv2.arcLength(cnt, True)
                    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                    if len(cnt) == 4 and cv2.contourArea(cnt) > self.minArea and cv2.isContourConvex(cnt):
                        cnt = cnt.reshape(-1, 2)
                        max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                        if max_cos < self.maxCos:
                            squares.append(cnt)
        return squares

    def detect(self, img):
        squares = self.find_squares(img)
        res = []
        for square in squares:
            if self.checkProportions(square):
                res.append(square)
        return res
        
        
        
        
        
        
        
