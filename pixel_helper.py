from PIL import ImageGrab
import numpy as np
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

def get_image(_top_left, _bot_right):
    _image = np.array(ImageGrab.grab(bbox=_top_left + _bot_right))
    _image = cv2.cvtColor(_image, cv2.COLOR_BGR2RGB)
    return _image

def get_text_from_screen(_top_left, _bot_right):
    _image = get_image(_top_left, _bot_right)
    _image = cv2.resize(_image, (0, 0), fx=2, fy=2)
    text = pytesseract.image_to_string(_image)
    if text == "":
        return "$0"
    return text

def show_text_from_screen(_top_left, _bot_right):
    _image = get_image(_top_left, _bot_right)
    _image = cv2.resize(_image, (0, 0), fx=2, fy=2)
    #_image = cv2.threshold(_image, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("test", _image)
    print("text:", pytesseract.image_to_string(_image))
    cv2.waitKey(0)

#absolute positions
def get_pixel_greyscale(x, y):
    gray_square = np.array(ImageGrab.grab([x - 1, y - 1, x + 1, y + 1]))
    gray_square = cv2.cvtColor(gray_square, cv2.COLOR_BGR2GRAY)
    return gray_square[1][1]

#relative position withing the buffer
def get_pixel_greyscale_from_buffer(buffer, x, y):
    gray_square = np.array(buffer)
    gray_square = cv2.cvtColor(gray_square, cv2.COLOR_BGR2GRAY)
    return gray_square[x][y]
