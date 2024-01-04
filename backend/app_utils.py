import cv2
import numpy as np
from digit_recognizer import digit_recognizer
import copy
import size_detection

def predict_numbers(boxes, model):
    numbers = []
    for box in boxes:
        # Preprocess the box image for YOLO
        box_img = cv2.resize(box, (640, 640))  # Adjust size if needed
        results = model(box_img)  # Run YOLO detection

        # Extract the predicted number
        if results.xyxy[0].shape[0] > 0:  # Check if any detections
            number_confidence, number_class, _, _ = results.xyxy[0][0].tolist()
            number = int(number_class)  # Convert class ID to number
            numbers.append(number)
        else:
            numbers.append(0)  # No detection, append 0

    return numbers


def preProcess(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)
    return imgThreshold


def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area


def reorder(points):
    points = points.reshape((4, 2))
    pointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = points.sum(1)
    pointsNew[0] = points[np.argmin(add)]
    pointsNew[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    pointsNew[1] = points[np.argmin(diff)]
    pointsNew[2] = points[np.argmax(diff)]
    return pointsNew


def splitBoxes(img, grid_size=9):
    rows = np.vsplit(img, grid_size)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, grid_size)
        for box in cols:
            boxes.append(box)
    return boxes


def print_sudoku_board(sudoku_board, grid_size):
    # Determine the width of each cell based on the grid_size
    cell_width = 2 + int(grid_size ** 0.5)

    # Print the Sudoku board
    for i in range(grid_size):
        if i > 0 and i % int(grid_size ** 0.5) == 0:
            print("-" * (cell_width * grid_size + int(grid_size ** 0.5) - 1))

        for j in range(grid_size):
            if j > 0 and j % int(grid_size ** 0.5) == 0:
                print("|", end=" ")

            value = sudoku_board[i * grid_size + j]

        print()


def find_size(frame):
    # Make a copy of the original frame
    original_frame = copy.deepcopy(frame)
    # Apply image processing to detect edges in the frame
    edges = size_detection.image_processing(frame)

    # Find contours in the edged image
    contours = size_detection.find_contours(edges)

    if contours:
        print('contours found')
        # Sort contours by area and find the largest contour (presumed Sudoku puzzle)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(contours[0], 0.02 * cv2.arcLength(contours[0], True), True)

        # Make a copy of the original frame
        original_frame = copy.deepcopy(frame)

        # Draw the contour on the original frame
        size_detection.draw_contour(frame, approx, size_detection.color_green)  # TO FIND SIZE
        size_detection.draw_contour(original_frame, approx, size_detection.color_black)  # TO CROP CELLS

        # If a Sudoku puzzle is detected (assuming 4 corners), proceed with further processing
        return size_detection.sudoku_puzzle_verification(frame, original_frame, approx)


def process_image(img, height_img, width_img, board_size):
    # img = cv2.imread(path_image)
    img = cv2.resize(img, (width_img, height_img))
    img_blank = np.zeros((height_img, width_img, 3), np.uint8)
    img_threshold = preProcess(img)

    # Finding the contours
    img_contours = img.copy()
    img_big_contour = img.copy()
    contours, hierarchy = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)

    # Finding the biggest contour
    biggest, max_area = biggestContour(contours)
    if biggest.size != 0:
        biggest = reorder(biggest)
        cv2.drawContours(img_big_contour, biggest, -1, (0, 0, 255), 10)
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0], [width_img, 0], [0, height_img], [width_img, height_img]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        img_warp_colored = cv2.warpPerspective(img, matrix, (width_img, height_img))
        img_detected_digits = img_blank.copy()
        img_warp_colored = cv2.cvtColor(img_warp_colored, cv2.COLOR_BGR2GRAY)

    img_solved_digits = img_blank.copy()
    boxes = splitBoxes(img_warp_colored, board_size)

    board = digit_recognizer(boxes, board_size)
    return board