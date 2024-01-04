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

  const getCellStyle = () => {
    const cellSize = boardSize === 9 ? "40px" : "30px" // Adjust as needed
    const margin = boardSize === 9 ? "10px" : "5px" // Adjust as needed

    return {
      width: "60px",
      height: cellSize,
      margin: `0 ${margin} ${margin} 0`,
    }
  }

  const saveToTxt = () => {
    const txtContent = board.map((row) => row.join(" ")).join("\n")
    const blob = new Blob([txtContent], { type: "text/plain" })
    const link = document.createElement("a")
    link.href = URL.createObjectURL(blob)
    link.download = "sudoku_board.txt"
    link.click()
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
      {!isSolved && (
        <Button
          variant='contained'
          onClick={saveToTxt}
          sx={{ marginBottom: 1 }}
        >
          Save to TXT
        </Button>
      )}

      <Stack
        direction='row'
        justifyContent='center'
        alignItems='center'
        spacing={2}
      >
        <Avatar
          sx={{ width: 400, height: 400, marginRight: 2 }}
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
                    sx={getCellStyle()}
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
