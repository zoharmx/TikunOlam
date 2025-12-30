/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#050507", // Casi negro, vacío profundo
        surface: "#0f111a",    // Superficie de tarjetas
        primary: "#3a86ff",    // Chochmah (Sabiduría/Tecnología)
        secondary: "#9d4edd",  // Keter (Corona/Ética)
        accent: "#06d6a0",     // Binah (Entendimiento/Análisis)

        // Sefirot Palette
        sef: {
          keter: "#ffffff",    // Corona (Luz pura)
          chochmah: "#3a86ff", // Sabiduría
          binah: "#06d6a0",    // Entendimiento
          chesed: "#ffd60a",   // Misericordia
          gevurah: "#e63946",  // Severidad
          tiferet: "#f77f00",  // Belleza (Equilibrio)
          netzach: "#06ffa5",  // Victoria
          hod: "#457b9d",      // Esplendor
          yesod: "#a8dadc",    // Fundamento
          malchut: "#6a4c93",  // Reino (Manifestación)
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        }
      }
    },
  },
  plugins: [],
}
