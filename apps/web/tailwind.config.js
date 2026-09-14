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
        background: '#030712',
        card: '#0b0f19',
        primary: '#06b6d4',
        accent: '#3b82f6',
      },
      animation: {
        'spin-slow': 'spin 12s linear infinite',
      },
    },
  },
  plugins: [],
}
