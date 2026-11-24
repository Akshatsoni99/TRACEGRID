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
        tg: {
          bg: "#F4F6F8",
          sidebar: "#142235",
          sidebarHover: "#1C2F47",
          sidebarActive: "#243B59",
          primary: "#245B88",
          primaryHover: "#1C4A70",
          text: "#172333",
          secondary: "#687586",
          border: "#DCE2E8",
          warning: "#D69A36",
          critical: "#BD4A4A",
          success: "#31846B",
          surface: "#FFFFFF",
          muted: "#EBF0F5"
        }
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
        mono: ["JetBrains Mono", "SFMono-Regular", "Consolas", "Liberation Mono", "monospace"]
      }
    },
  },
  plugins: [],
}

