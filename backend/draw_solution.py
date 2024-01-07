import cv2
import numpy as np
import imutils
# from tensorflow.keras.models import load_model
import imutils
from keras.src.saving.saving_api import load_model

from app_utils import process_image
from solver import solve


def find_board(img):
    """Takes an image as input and finds a sudoku board inside of the image"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 13, 20, 20)
    edged = cv2.Canny(bfilter, 30, 180)
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE,
    cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    newimg = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 3)
    # cv2.imshow("Contour.png", newimg)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    location = None
    # Finds rectangular contour
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 15, True)
        if len(approx) == 4:
            location = approx
            break

    result = get_perspective(img, location)
    # Rotate the image 90 degrees counter-clockwise
    # result = cv2.rotate(result, cv2.ROTATE_90_CLOCKWISE)

    return result, location

def get_perspective(img, location, height = 576, width = 576):
    """Takes an image and location of an interesting region.
    And return the only selected region with a perspective transformation"""
    pts1 = np.float32([location[0], location[3], location[1], location[2]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result


# split the board into 81 individual images
# split the board into 81 individual images
def split_boxes(board, board_size):
    """Takes a sudoku board and split it into 81 cells.
    each cell contains an element of that board either given or an empty cell."""
    rows = np.vsplit(board,board_size)
    boxes = []
    for r in rows:
        cols = np.hsplit(r,board_size)
        for box in cols:
            box = cv2.resize(box, (576, 576))/255.0
            cv2.imshow("Splitted block", box)
            cv2.waitKey(50)
            boxes.append(box)
    return boxes


def displayNumbers(img, numbers, board_size, color=(0, 255, 0), font=cv2.FONT_HERSHEY_COMPLEX, fontScale=1.5, thickness=2):
    W = int(img.shape[1]/board_size)  # Width of each cell
    H = int(img.shape[0]/board_size)  # Height of each cell

    for i in range(board_size):
        for j in range(board_size):
            num = numbers[(j*board_size)+i]
            if num != 0:
                text = str(num)

                # Get the text size
                if(board_size == 16):
                    fontScale = 0.75
                textSize = cv2.getTextSize(text, font, fontScale, thickness)[0]

                # Calculate the text position so that it's centered
                posX = int((i*W + W/2) - textSize[0]/2)
                posY = int((j*H + H/2) + textSize[1]/2)

                cv2.putText(img, text, (posX, posY), font, fontScale, color, thickness, cv2.LINE_AA)

    return img

def get_InvPerspective(img, masked_num, location, height = 576, width = 576):
    """Takes original image as input"""
    pts1 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    pts2 = np.float32([location[0], location[3], location[1], location[2]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(masked_num, matrix, (img.shape[1],
    img.shape[0]))

    return result
