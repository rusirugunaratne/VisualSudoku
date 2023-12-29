import { colors } from "../utils/colors"

export const themeOptions = {
  typography: {
    fontFamily: `"Poppins", "Helvetica", "Arial", sans-serif`,
    fontSize: 14,
    fontWeightLight: 300,
    fontWeightRegular: 400,
    fontWeightMedium: 500,
  },
  palette: {
    type: "light",
    primary: {
      main: colors.primary,
    },
    secondary: {
      main: "#f50057",
    },
    background: {
      paper: "white",
    },
  },
  shape: {
    borderRadius: 0,
  },
  overrides: {
    MuiButton: {
      contained: {
        boxShadow: "none", // Remove the box shadow for contained buttons
      },
      outlined: {
        boxShadow: "none", // Remove the box shadow for outlined buttons
      },
      text: {
        paddingX: 8,
        paddingY: 3,
      },
    },
  },
}
