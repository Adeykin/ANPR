import cv2
import numpy as np

class Warper:
    def __init__(self, size=(253,50)):
        self.size = size #target plate size after rescale
    
    def warp(self, img, rect):
        srcTri = np.float32([rect[0], rect[1], rect[3]])
        dstTri = np.float32([(0, 0), (self.size[0], 0), (0, self.size[1]) ])
        warpMat = cv2.getAffineTransform( srcTri, dstTri );
        warped = cv2.warpAffine( img, warpMat, self.size );
        return warped
