import { CssBaseline, ThemeProvider, createTheme } from "@mui/material"
import "./App.css"
import { MainScreen } from "./components/MainScreen"
import { themeOptions } from "./theme/CustomTheme"

function App() {
  const theme = createTheme(themeOptions)
  return (
    <>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <MainScreen />
      </ThemeProvider>
    </>
  )
}

export default App
