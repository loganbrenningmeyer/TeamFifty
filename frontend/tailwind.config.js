/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'bg-grey': '#121212',
        'custom-blue': '#203749',
        'button-blue': 'rgb(23, 146, 217)',
        'button-blue-hover': 'rgb(16, 106, 159)'
      },
    },
  },
  plugins: [],
}