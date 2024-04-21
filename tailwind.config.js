const defaultTheme = require('tailwindcss/defaultTheme')
export default {
    theme: {
      extend: {
        fontFamily: {
          inter: ['Inter', ...defaultTheme.fontFamily.sans],
        },
        colors: {
          'light-blue': '#75BDFF',
          'dark-blue': '#240053',
          'light-gray': '#F0F3F6',
          'star-gray': '#D9D9D9',
          yellow: '#FBFF47',
          'word-blue': '#4BA9FF',
          gray: '#4B4B4B',
          red: '#FF0000',
          orange: '#FF9900',
          green: '#9EFF23',
          cyan: '#00FFE0'
        }

      }
    },
    plugins: [],
    content: [
      `./components/**/*.{vue,js,ts}`,
      `./layouts/**/*.vue`,
      `./pages/**/*.vue`,
      `./composables/**/*.{js,ts}`,
      `./plugins/**/*.{js,ts}`,
      `./utils/**/*.{js,ts}`,
      `./App.{js,ts,vue}`,
      `./app.{js,ts,vue}`,
      `./Error.{js,ts,vue}`,
      `./error.{js,ts,vue}`,
      `./app.config.{js,ts}`
    ]
  }