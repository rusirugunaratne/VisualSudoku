import {
  Avatar,
  Button,
  Stack,
  ToggleButton,
  ToggleButtonGroup,
} from "@mui/material"
import PhotoCamera from "@mui/icons-material/PhotoCamera"
import GridViewIcon from "@mui/icons-material/GridView"
import ClearIcon from "@mui/icons-material/Clear"
import React, { useState } from "react"
import Webcam from "react-webcam"

function UploadSection({
  imageFileG,
  setImageFileG,
  handleInputImage,
  handleBoardTypeChange,
  boardType,
  predict,
  setFile,
}) {
  const [captureMode, setCaptureMode] = useState("file") // "file" or "webcam"

  const videoConstraints = {
    width: 600,
    height: 600,
    facingMode: "user",
  }

  const handleCaptureModeChange = (event, newMode) => {
    if (newMode !== null) {
      setCaptureMode(newMode)
    }
  }

  const handleWebcamCapture = () => {
    // Access the webcam screenshot using the getScreenshot callback
    const imageSrc = webcamRef.current.getScreenshot()
    console.log(imageSrc)

    // Extract base64 data from the imageSrc string
    const base64Image = imageSrc.split(",")[1]

    if (base64Image) {
      try {
        // Decode the base64 string
        const decodedImage = atob(base64Image)

        // Convert the decoded string to a Uint8Array
        const arrayBuffer = new ArrayBuffer(decodedImage.length)
        const uint8Array = new Uint8Array(arrayBuffer)

        for (let i = 0; i < decodedImage.length; i++) {
          uint8Array[i] = decodedImage.charCodeAt(i)
        }

        // Create a Blob from the Uint8Array
        const blob = new Blob([uint8Array], { type: "image/jpeg" })

        // Create a File from the Blob
        const imageFile = new File([blob], "webcam_capture.jpeg", {
          type: "image/jpeg",
        })

        // Use the captured image as needed (e.g., set it in state)
        setImageFileG({ imageFile, image: imageSrc })

        // Call the predict function here
        predict(imageFile)
      } catch (error) {
        console.error("Error decoding base64 image:", error)
      }
    }
  }

  // Function to convert base64 to Blob
  const dataURItoBlob = (dataURI) => {
    const byteString = atob(dataURI)
    const mimeString = "image/jpeg"

    const ab = new ArrayBuffer(byteString.length)
    const ia = new Uint8Array(ab)

    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i)
    }

    return new Blob([ab], { type: mimeString })
  }

  const webcamRef = React.useRef(null)

  return (
    <Stack
      direction='column'
      justifyContent='center'
      alignItems='center'
      spacing={2}
    >
      {/* <ToggleButtonGroup
        color='primary'
        value={boardType}
        exclusive
        onChange={handleBoardTypeChange}
        aria-label='Platform'
      >
        <ToggleButton value='9x9'>9x9</ToggleButton>
        <ToggleButton value='16x16'>16x16</ToggleButton>
      </ToggleButtonGroup> */}
      <Avatar
        sx={{ width: 200, height: 200 }}
        variant='rounded'
        src={imageFileG.image}
      >
        <GridViewIcon />
      </Avatar>
      <Stack direction={"row"} spacing={2}>
        <ToggleButtonGroup
          value={captureMode}
          exclusive
          onChange={handleCaptureModeChange}
        >
          <ToggleButton value='file'>File</ToggleButton>
          <ToggleButton value='webcam'>Webcam</ToggleButton>
        </ToggleButtonGroup>
      </Stack>

      {imageFileG.imageFile && (
        <Button startIcon={<ClearIcon />} onClick={() => setImageFileG("")}>
          Clear
        </Button>
      )}

      {captureMode === "file" ? (
        <Button
          startIcon={<PhotoCamera />}
          variant='contained'
          component='label'
        >
          Upload Image
          <input
            hidden
            name='image'
            accept='image/*'
            type='file'
            onChange={handleInputImage}
          />
        </Button>
      ) : (
        <Webcam
          audio={false}
          height={200}
          screenshotFormat='image/jpeg'
          width={200}
          videoConstraints={videoConstraints}
          ref={webcamRef}
        >
          {({ getScreenshot }) => (
            <Button variant='contained' onClick={handleWebcamCapture}>
              Capture photo
            </Button>
          )}
        </Webcam>
      )}
    </Stack>
  )
}

export default UploadSection
