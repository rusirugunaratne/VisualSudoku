import { Button, Stack, Typography } from "@mui/material"

function SetBoardSize({ boardType, readBoard }) {
  return (
    <Stack
      direction='column'
      justifyContent='center'
      alignItems='center'
      spacing={2}
    >
      <Typography variant='h4'>Detected Board Size : {boardType}</Typography>
      <Button
        onClick={() => readBoard(boardType === "9x9" ? 9 : 16)}
        variant='contained'
      >
        That is Correct
      </Button>
      <Button
        onClick={() => readBoard(boardType === "9x9" ? 16 : 9)}
        variant='contained'
      >
        Change it to {boardType === "9x9" ? "16x16" : "9x9"}
      </Button>
    </Stack>
  )
}

export default SetBoardSize
