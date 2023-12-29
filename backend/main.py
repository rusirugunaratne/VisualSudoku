from app_utils import process_image
from fastapi import FastAPI, File, UploadFile
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from pydantic import BaseModel
from typing import Optional


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


class SudokuBoard(BaseModel):
    file: UploadFile = File(...)
    board_size: Optional[int] = 9

@app.get('/ping')
async def ping():
    return 'Hello, I am alive'


async def read_file_as_image(data) -> np.ndarray:
    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    return image


@app.post('/api/read_board')
async def read_image(file: UploadFile = File(...), board_size: int = 16):
    contents = await file.read()
    image = await read_file_as_image(contents)

    print('board_size', board_size)

    height_img = 576
    width_img = 576

    result_board = process_image(image, height_img, width_img, board_size)
    return {"result": result_board.tolist()}


# def main():
#     path_image = "resources/16.png"
#     height_img = 576
#     width_img = 576
#     board_size = 16
#
#     result_board = process_image(path_image, height_img, width_img, board_size)
#     print(result_board)


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
