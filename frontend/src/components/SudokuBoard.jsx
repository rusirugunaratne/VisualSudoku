import React, { useEffect, useState } from "react"
import { TextField, Stack, Button, Typography, Avatar } from "@mui/material"

const SudokuBoard = ({ boardSize, elements, imageFileG, isSolved }) => {
  const [board, setBoard] = useState(
    elements.length
      ? elements
      : Array.from({ length: boardSize }, () => Array(boardSize).fill(""))
  )

  const handleInputChange = (row, col, event) => {
    const updatedBoard = [...board]
    updatedBoard[row][col] = parseInt(event.target.value) || "" // Ensure empty strings for non-numeric values
    setBoard(updatedBoard)
  }

  const getCellStyle = (value) => {
    const cellSize = boardSize === 9 ? "40px" : "30px"
    const margin = boardSize === 9 ? "10px" : "5px"
    const baseStyle = {
      width: "60px",
      height: cellSize,
      margin: `0 ${margin} ${margin} 0`,
    }

    // Add conditional style for values greater than 16
    if (value > 16) {
      return {
        ...baseStyle,
        background: "red",
      }
    }

    return baseStyle
  }

  const saveToTxt = async () => {
    try {
      const fileHandle = await window.showSaveFilePicker({
        suggestedName: "sudoku_board.txt",
        types: [
          {
            accept: {
              "text/plain": [".txt"],
            },
          },
        ],
      })

      const writable = await fileHandle.createWritable()
      await writable.write(board.map((row) => row.join(" ")).join("\n"))
      await writable.close()
    } catch (error) {
      console.error("Error saving file:", error)
    }
  }

  const solveSudoku = () => {
    // Implement your Sudoku-solving logic here
    // Console log the edited Sudoku board
    console.log(board)
  }

  return (
    <div className='sudoku-board'>
      {!isSolved && (
        <Typography variant='h4'>Edit the detected values</Typography>
      )}

      {isSolved && <Typography variant='h4'>Solution</Typography>}
      {isSolved && (
        <>
          <TextField
            multiline
            rows={boardSize}
            fullWidth
            value={elements.map((row) => row.join(" ")).join("\n")}
            variant='outlined'
            sx={{ marginBottom: 2 }}
          />
        </>
      )}
      {!isSolved && (
        <Button
          variant='contained'
          onClick={saveToTxt}
          sx={{ marginBottom: 1 }}
        >
          Save to TXT
        </Button>
      )}

      {!isSolved && (
        <Button
          variant='contained'
          onClick={saveToTxt}
          sx={{ marginBottom: 1 }}
        >
          Upload Solution
        </Button>
      )}

      <Stack
        direction='row'
        justifyContent='center'
        alignItems='center'
        spacing={2}
      >
        <Avatar
          sx={{ width: 400, height: "auto", marginRight: 2 }}
          variant='rounded'
          src={imageFileG.image}
        />
        {!isSolved && (
          <Stack
            direction='column'
            justifyContent='center'
            alignItems='center'
            spacing={2}
          >
            {board.map((row, i) => (
              <Stack
                key={i}
                direction='row'
                spacing={1}
                justifyContent='center'
                marginBottom={1} // Adjust the margin as needed
              >
                {row.map((value, j) => (
                  <TextField
                    key={`${i}-${j}`}
                    type='text'
                    value={value}
                    onChange={(e) => handleInputChange(i, j, e)}
                    variant='outlined'
                    size='small'
                    sx={getCellStyle(value)}
                  />
                ))}
              </Stack>
            ))}
          </Stack>
        )}
      </Stack>
    </div>
  )
}

export default SudokuBoard
