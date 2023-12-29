import React, { useEffect, useState } from "react"
import { TextField, Stack } from "@mui/material"

const SudokuBoard = ({ boardSize, elements }) => {
  const [board, setBoard] = useState(
    elements.length
      ? elements
      : Array.from({ length: boardSize }, () => Array(boardSize).fill(""))
  )

  const handleInputChange = (row, col, event) => {
    const updatedBoard = [...board]
    updatedBoard[row][col] = parseInt(event.target.value)
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

  useEffect(() => {}, [boardSize, elements])

  const renderBoard = () => {
    return board.map((row, i) => (
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
            fullWidth
            sx={getCellStyle()}
          />
        ))}
      </Stack>
    ))
  }

  return <div className='sudoku-board'>{renderBoard()}</div>
}

export default SudokuBoard
