/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
    keyframes: {
      pulseGlow: {
        '0%, 100%': { boxShadow: '0 0 5px 4px rgba(56, 189, 248, 0.5)' },
        '50%': { boxShadow: '0 0 10px 6px rgba(56, 189, 248, 0.8)' },
      },
      tiltWithPause: {
        '0%': { transform: 'rotate(0deg)' },
        '10%': { transform: 'rotate(-10deg)' },
        '20%': { transform: 'rotate(10deg)' },
        '30%': { transform: 'rotate(0deg)' },
        '100%': { transform: 'rotate(0deg)' }, /* Ensure it resets */
      },
    },
    animation: {
      pulseGlow: 'pulseGlow 2s infinite',
      tiltWithPause: 'tiltWithPause 6s ease-in-out infinite',
    },
  },
  plugins: [],
};
