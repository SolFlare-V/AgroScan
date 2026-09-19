/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'agro-dark': '#0a2e1a',
        'agro-terminal': '#00ff88',
        'agro-amber': '#f59e0b',
        'agro-text': '#f0fdf4',
      },
      fontFamily: {
        'grotesk': ['"Space Grotesk"', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
      },
      backgroundImage: {
        'glass-gradient': 'linear-gradient(135deg, rgba(10, 46, 26, 0.7), rgba(0, 255, 136, 0.05))',
      },
      boxShadow: {
        'glow-green': '0 0 15px -3px rgba(0, 255, 136, 0.3)',
        'glow-amber': '0 0 15px -3px rgba(245, 158, 11, 0.3)',
      }
    },
  },
  plugins: [],
}
