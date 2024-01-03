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
      console.log("board new inside", boardType)
      setLoading(true)
      const formData = new FormData()
      formData.append("file", imageFile)
      // formData.append("board_size", boardType === "9x9" ? 9 : 16)

      formData.append("board", { board_size: boardType === "9x9" ? 9 : 16 })

      createAPIEndpoint(ENDPOINTS.readBoard)
        .post(formData)
        .then((r) => {
          setBoardElements(r.data.result)
          console.log("data", r.data.result)
          setLoading(false)
        })
        .catch((err) => console.log(err))
    },
    [file, boardType]
  )

  const solve = () => {
    const formData = new FormData()
    const reader = new FileReader()
    const image = imageFileG.imageFile
    reader.readAsDataURL(image)
    formData.append("file", image)
    formData.append("board_size", boardType === "9x9" ? 9 : 16)

    // Send board_values as part of the request body
    formData.append(
      "board_values",
      JSON.stringify(
        boardElements.map((row) => row.map((val) => parseInt(val)))
      )
    )

    createAPIEndpoint(ENDPOINTS.solveBoard)
      .post(formData)
      .then((r) => {
        setSolvedImage(r.data.result_image)
      })
      .catch((err) => console.log(err))
  }

  console.log("board new", boardType)

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
              />
              <Button variant='contained' onClick={solve} sx={{ marginTop: 2 }}>
                Solve
              </Button>
              {solvedImage && (
                <Avatar
                  sx={{ width: 250, height: 250, marginTop: 2 }}
                  variant='rounded'
                  src={`data:image/png;base64,${solvedImage}`}
                />
              )}
            </>
          )}
        </Stack>
      </Stack>
    </>
  )
}
