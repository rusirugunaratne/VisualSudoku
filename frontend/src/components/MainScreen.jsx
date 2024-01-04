import React, { useCallback, useEffect, useState } from "react"
import {
  Avatar,
  Box,
  Button,
  CircularProgress,
  Stack,
  Typography,
} from "@mui/material"
import { ENDPOINTS, createAPIEndpoint } from "../api/api"
import UploadSection from "./UploadSection"
import SudokuBoard from "./SudokuBoard"
import logo from "../assets/sudokuLogo.png"

export function MainScreen() {
  const [file, setFile] = useState({})
  const [imageFileG, setImageFileG] = useState({})
  const [boardType, setBoardType] = React.useState("9x9")
  const [boardElements, setBoardElements] = useState([])
  const [loading, setLoading] = useState(false)
  const [solvedImage, setSolvedImage] = useState(null)
  const [isSolved, setIsSolved] = useState(false)

  const handleBoardTypeChange = (event, newBoard) => {
    setBoardType(newBoard)
  }

  useEffect(() => {
    console.log("board", boardElements)
  }, [boardType, boardElements])

  useEffect(() => {}, [file, imageFileG, loading, boardElements])

  function objectToFormData(obj) {
    const formData = new FormData()

    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        formData.append(key, obj[key].toString())
      }
    }

    return formData
  }

  const predict = useCallback(
    async (imageFile) => {
      setLoading(true)
      const formData = new FormData()
      formData.append("file", imageFile)

      createAPIEndpoint(ENDPOINTS.readBoard)
        .post(formData)
        .then((r) => {
          // Determine the size of the Sudoku board based on the result
          const numRows = r.data.result.length
          const numColumns = r.data.result[0].length

          let newBoardType = "9x9" // Default to "9x9"
          if (numRows === 16 && numColumns === 16) {
            newBoardType = "16x16"
          }

          // Update the boardType state based on the size of the Sudoku board
          setBoardType(newBoardType)

          // Update the boardElements state
          setBoardElements(r.data.result)

          setLoading(false)
        })
        .catch((err) => {
          console.log(err)
          setLoading(false)
        })
    },
    [file, boardType]
  )

  const solve = () => {
    const formData = new FormData()

    // Convert boardElements to a 2D array of integers
    const boardValues = boardElements.map((row) =>
      row.map((val) => parseInt(val))
    )

    // Append board_values as a JSON string to the FormData
    formData.append("board_values", JSON.stringify(boardValues))

    createAPIEndpoint(ENDPOINTS.solveBoard)
      .post(boardValues)
      .then((r) => {
        setSolvedImage(r.data.result_image)
        setImageFileG({ image: `data:image/png;base64,${r.data.result_image}` })
        setBoardElements([...r.data.solved])
        setIsSolved(true)
      })
      .catch((err) => console.log(err))
  }

  console.log("board new", boardElements)

  const handleInputImage = (e) => {
    if (e.target.files && e.target.files[0]) {
      let imageFile = e.target.files[0]
      setFile(e.target.files[0])
      let formValues = {}
      const reader = new FileReader()

      reader.onload = (x) => {
        setImageFileG({ imageFile: imageFile, image: x.target?.result })
        formValues = { file: x.target?.result }
      }
      reader.readAsDataURL(imageFile)
      predict(imageFile)
    }
  }

  return (
    <>
      <Stack
        direction='column'
        justifyContent='center'
        alignItems='center'
        spacing={2}
      >
        <img src={logo} width={400} alt='' srcset='' />

        <Stack direction={"row"} spacing={2}>
          {loading === false && boardElements.length === 0 && (
            <UploadSection
              imageFileG={imageFileG}
              handleInputImage={handleInputImage}
              setImageFileG={setImageFileG}
              boardType={boardType}
              handleBoardTypeChange={handleBoardTypeChange}
              predict={predict}
              setFile={setFile}
            />
          )}

          {loading && (
            <Box sx={{ display: "flex" }}>
              <CircularProgress />
            </Box>
          )}

          {boardType && boardElements.length !== 0 && (
            <>
              <SudokuBoard
                boardSize={boardType === "9x9" ? 9 : 16}
                elements={boardElements}
                imageFileG={imageFileG}
                isSolved={isSolved}
              />
              {!isSolved && (
                <Button
                  variant='contained'
                  onClick={solve}
                  sx={{ marginTop: 2 }}
                >
                  Solve
                </Button>
              )}
            </>
          )}
        </Stack>
      </Stack>
    </>
  )
}
