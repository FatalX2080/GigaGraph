import cv2
import os
import numpy as np
from typing import Optional

NAME = "Граф1.jpg"
PATH = "/home/max/Изображения/Снимки экрана"
BAD_RANGE = ((0, 0, 0), (255, 255, 170))

def open_img(path: str, name: str) -> Optional[np.ndarray]:
    full_path = os.path.join(path, name)
    if os.path.isfile(full_path) and os.path.exists(full_path):
        return cv2.imread(full_path)
    return np.zeros((100, 100), np.uint8)


def prepare_photo(photo: np.ndarray, bad_range:tuple[tuple, tuple]) -> np.ndarray:
    hsv = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)
    ranged_img = cv2.inRange(hsv, np.array(bad_range[0]), np.array(bad_range[1]))
    res = cv2.bitwise_not(ranged_img)
    return res


def recognize(photo: np.ndarray, base_photo: np.ndarray) -> np.ndarray:
    contours, _ = cv2.findContours( photo.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if len(cnt) > 6:
            ellipse = cv2.fitEllipse(cnt)
            cv2.ellipse(base_photo, ellipse, (0, 0, 255), 2)

    return base_photo


im = open_img(PATH, NAME)
im1 = prepare_photo(im, BAD_RANGE)
im2 = recognize(im1, im.copy())

cv2.imshow("test", im)
cv2.imshow("prepared", im1)
cv2.imshow("recognized", im2)
cv2.waitKey(0)
