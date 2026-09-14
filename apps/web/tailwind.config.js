/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#090a0f',
        card: '#12151e',
        primary: '#3b82f6',
        accent: '#8b5cf6',
        cyanAccent: '#06b6d4',
      },
    },
  },
  plugins: [],
}
