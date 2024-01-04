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
def split_boxes(board):
    """Takes a sudoku board and split it into 81 cells.
    each cell contains an element of that board either given or an empty cell."""
    rows = np.vsplit(board,9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r,9)
        for box in cols:
            box = cv2.resize(box, (576, 576))/255.0
            cv2.imshow("Splitted block", box)
            cv2.waitKey(50)
            boxes.append(box)
    return boxes


def displayNumbers(img, numbers, color=(0, 255, 0), font=cv2.FONT_HERSHEY_COMPLEX, fontScale=1.5, thickness=2):
    W = int(img.shape[1]/9)  # Width of each cell
    H = int(img.shape[0]/9)  # Height of each cell

    for i in range(9):
        for j in range(9):
            num = numbers[(j*9)+i]
            if num != 0:
                text = str(num)

                # Get the text size
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


# board, location = find_board(img)
# cv2.imshow("Board", board)
#
# height_img = 576
# width_img = 576
# board_size = 9
#
# original_board, img = process_image(path_image, height_img, width_img, board_size)
# print(original_board)
#
# solved_board_nums = solve(original_board)
#
# # get only solved numbers for the solved board
# flat_solved_board_nums = solved_board_nums.flatten()
# print(flat_solved_board_nums)
#
# # Create a binary mask - 1 where there is a solved number, 0 otherwise
# # binArr = (flat_solved_board_nums > 0).astype(int)
#
# # Use the binary mask to get only the solved numbers
# # flat_solved_board_nums = flat_solved_board_nums * binArr
#
# # create a mask
# mask = np.zeros_like(board)
# solved_board_mask = displayNumbers(mask, flat_solved_board_nums)
# # Rotate the image 90 degrees counter-clockwise
# solved_board_mask = cv2.rotate(solved_board_mask, cv2.ROTATE_90_COUNTERCLOCKWISE)
# # cv2.imshow("Solved Mask", solved_board_mask)
#
# # Get inverse perspective
# inv = get_InvPerspective(img, solved_board_mask, location)
#
# combined = cv2.addWeighted(img, 0.5, inv, 1, 0)
# cv2.imshow("Final result", combined)
#
# # cv2.imshow("Board", board)
# cv2.waitKey(0)
# cv2.destroyAllWindows()