/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        agri: {
          50: '#f2f9f4',
          100: '#e1f2e6',
          200: '#c5e4ce',
          300: '#9acfad',
          400: '#68b284',
          500: '#439562',
          600: '#32784d',
          700: '#29603f',
          800: '#244d34',
          900: '#1e402c',
          950: '#0e2417',
        },
        earth: {
          50: '#faf6f0',
          100: '#f3eadf',
          200: '#e6d3bd',
          300: '#d5b796',
          400: '#c39870',
          500: '#b48154',
          600: '#a46e48',
          700: '#89573c',
          800: '#6f4735',
          900: '#5a3b2e',
        }
      }
    },
  },
  plugins: [],
}
