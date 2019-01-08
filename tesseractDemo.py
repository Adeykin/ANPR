import pytesseract
import cv2
from PIL import Image

path = '/home/adeykin/projects/ANPR/others/plate_recognition/test_data/A002HY163.png'

img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

#pytesseract.setVariable("tessedit_char_whitelist","0123456789ABCETYOPHXM");

print pytesseract.image_to_string(img)
print pytesseract.image_to_boxes(img)

crop = img[6:46, 12:170]

print pytesseract.image_to_string(crop, config='-c tessedit_char_whitelist=0123456789ABCETYOPHXM')
print pytesseract.image_to_boxes(crop)
#print pytesseract.image_to_osd(crop)

#cv2.imshow('win', crop)
#cv2.waitKey()


