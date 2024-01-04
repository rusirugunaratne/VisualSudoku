import base64

from app_utils import process_image, find_size
from fastapi import FastAPI, File, UploadFile, Form
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import json
from pydantic import BaseModel
from typing import Optional, List
from fastapi import HTTPException
from draw_solution import find_board, displayNumbers, get_InvPerspective
from solver import solve
import copy

app = FastAPI()

IMAGE = None
BOARD_SIZE = 0

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/ping')
async def ping():
    return 'Hello, I am alive'


async def read_file_as_image(data) -> np.ndarray:
    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    global IMAGE
    IMAGE = image

    return image


class ImageUpload(BaseModel):
    board_size: int = Form(...)


@app.post('/api/read_board')
async def read_image(file: UploadFile):
    contents = await file.read()
    image = await read_file_as_image(contents)

    height_img = 576
    width_img = 576

    board_size = find_size(copy.deepcopy(image))
    print('board_size', board_size)
    global BOARD_SIZE
    BOARD_SIZE = board_size

    result_board = process_image(image, height_img, width_img, board_size)
    return {"result": result_board.tolist()}




@app.post('/api/solve_board')
async def solve_board(board_values: List[List[int]]):
    global BOARD_SIZE
    global IMAGE
    print('rec', board_values)
    bvals = board_values
    print('bvals', BOARD_SIZE)

    height_img = 576
    width_img = 576

    solved_board_nums = solve(board_values)
    sbnums = np.array(solved_board_nums)
    flat_solved_board_nums = sbnums.flatten()
    print(flat_solved_board_nums)

    board, location = find_board(IMAGE)

    mask = np.zeros_like(board)
    solved_board_mask = displayNumbers(mask, flat_solved_board_nums)
    # Rotate the image 90 degrees counter-clockwise
    solved_board_mask = cv2.rotate(solved_board_mask, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # cv2.imshow("Solved Mask", solved_board_mask)

    # Get inverse perspective
    inv = get_InvPerspective(IMAGE, solved_board_mask, location)

    combined = cv2.addWeighted(IMAGE, 0.5, inv, 1, 0)

    combined = cv2.addWeighted(IMAGE, 0.5, inv, 1, 0)

    _, result_image_bytes = cv2.imencode(".png", combined)
    result_image_base64 = base64.b64encode(result_image_bytes).decode('utf-8')

    return {"result_image": result_image_base64, "solved": solved_board_nums}


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
