from app_utils import process_image
from fastapi import FastAPI, File, UploadFile
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import json
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

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
    return image

@app.post('/api/read_board')
async def read_image(file: UploadFile, board_size: int = 9):
    contents = await file.read()
    image = await read_file_as_image(contents)

    print('board_size', board_size)

    height_img = 576
    width_img = 576

    result_board = process_image(image, height_img, width_img, board_size)
    return {"result": result_board.tolist()}

from fastapi import HTTPException

@app.post('/api/solve_board')
async def solve_board(board_values: str = "", file: UploadFile = File(...), board_size: int = 9):
    print('rec', board_values)
    bvals = board_values
    print('bvals', board_size)
    try:
        # Attempt to parse the JSON string to a list
        board_values_list = json.loads(board_values)
    except json.JSONDecodeError:
        # If parsing fails, return an HTTPException with a 400 Bad Request status
        raise HTTPException(status_code=400, detail="Invalid JSON format for board_values")

    contents = await file.read()
    image = await read_file_as_image(contents)

    height_img = 576
    width_img = 576

    result_image = process_image(image, height_img, width_img, board_size, board_values_list)
    # Add your logic here to solve the board using the provided values

    # You can return the result image as bytes
    _, result_image_bytes = cv2.imencode(".png", result_image)
    return {"result_image": result_image_bytes.tobytes()}


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
