/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin');

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
      slideInOut1: {
        '0%': { transform: 'translateX(2rem)' },
        '50%': { transform: 'translateX(96rem)' },
        '100%': { transform: 'translateX(2rem)' },
      },
      slideInOut2: {
        '0%': { transform: 'translateX(-96rem)' },
        '50%': { transform: 'translateX(-2rem)' },
        '100%': { transform: 'translateX(-96rem)' },
      },
      slideInOut3: {
        '0%': { transform: 'translateX(90rem)' },
        '50%': { transform: 'translateX(-20rem)' },
        '100%': { transform: 'translateX(90rem)' },
      },
    },
    animation: {
      pulseGlow: 'pulseGlow 2s infinite',
      tiltWithPause: 'tiltWithPause 6s ease-in-out infinite',
      slide1: 'slideInOut1 2s linear infinite',
      slide2: 'slideInOut2 2s linear infinite',
      slide3: 'slideInOut3 2s linear infinite',
    },
  },
  plugins: [
    plugin(function({ addUtilities }) {
      addUtilities({
        '.transition-transform': {
          transitionProperty: 'transform',
        },
      });
    }),
  ],
};
