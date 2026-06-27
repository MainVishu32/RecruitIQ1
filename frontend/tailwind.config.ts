import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#050505",
        surface: "#111111",
        surfaceHighlight: "#1a1a1a",
        primary: "#ffffff",
        muted: "#888888",
        accent: "#3b82f6", // Subtle blue for AI actions
        success: "#10b981",
        danger: "#ef4444",
        warning: "#f59e0b",
      },
      backgroundImage: {
        'glass-gradient': 'linear-gradient(180deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.0) 100%)',
      }
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;