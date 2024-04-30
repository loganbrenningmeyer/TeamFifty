/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'bg-grey': '#121212',
        'custom-blue': '#203749'
      },
    },
  },
  plugins: [],
}