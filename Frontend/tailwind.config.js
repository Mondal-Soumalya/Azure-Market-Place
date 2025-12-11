/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Blue AI Theme (Dark Mode - Default) - updated to professional brand system (legacy keys retained for compatibility)
        'bg-primary': '#0f0f23',
        'bg-secondary': '#181832',
        'bg-tertiary': '#242449',
        'border-color': '#334155',
        'text-primary': '#f1f5f9',
        'text-secondary': '#cbd5e1',
        'text-muted': '#94a3b8',
        // Legacy accent-* keys now map to brand primary / secondary (teal deprecated)
        'accent-primary': '#6366f1',
        'accent-primary-tint': 'rgba(99,102,241,0.12)',
        'accent-secondary': '#8b5cf6',
        'accent-secondary-tint': 'rgba(139,92,246,0.12)',
        'shadow-color': 'rgba(0,0,0,0.5)',
        
        // Status Colors (Dark Mode) aligned with design tokens states
        'success-bg': 'rgba(47,175,114,0.12)',
        'success-text': '#2FAF72',
        'success-border': '#2FAF72',
        'error-bg': 'rgba(209,75,85,0.12)',
        'error-text': '#D14B55',
        'error-border': '#D14B55',
        'info-bg': 'rgba(60,141,255,0.12)',
        'info-text': '#3C8DFF',
        'info-border': '#3C8DFF',
        'disabled-bg': '#1f2531',
        'disabled-text': '#6e7d88',

        // Light Mode Variables (refined to professional palette)
        'lm-bg-primary': '#f5f7fa',
        'lm-bg-secondary': '#ffffff',
        'lm-bg-tertiary': '#edf1f5',
        'lm-border-color': '#dce2e8',
        'lm-text-primary': '#0f172a',
        'lm-text-secondary': '#475569',
        'lm-text-muted': '#64748b',
        'lm-accent-primary': '#4f46e5',
        'lm-accent-primary-tint': 'rgba(79,70,229,0.12)',
        'lm-accent-secondary': '#7c3aed',
        'lm-accent-secondary-tint': 'rgba(124,58,237,0.12)',
        'lm-shadow-color': 'rgba(15,23,42,0.15)',

        // Light Mode Status Colors
        'lm-success-bg': 'rgba(47,175,114,0.12)',
        'lm-success-text': '#2FAF72',
        'lm-success-border': '#2FAF72',
        'lm-error-bg': 'rgba(209,75,85,0.12)',
        'lm-error-text': '#D14B55',
        'lm-error-border': '#D14B55',
        'lm-info-bg': 'rgba(60,141,255,0.12)',
        'lm-info-text': '#3C8DFF',
        'lm-info-border': '#3C8DFF',
        'lm-disabled-bg': '#e4eaf0',
        'lm-disabled-text': '#8e9ca7',
      },
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
      },
      animation: {
        'bounce-slow': 'bounce 2s infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite alternate',
        'fade-in-slide-up': 'fadeInSlideUp 0.5s ease-out',
        'typed-blink': 'typedjsBlink 1s infinite',
      },
      keyframes: {
        'bounce': {
          '0%, 20%, 50%, 80%, 100%': { transform: 'translateY(0)' },
          '40%': { transform: 'translateY(-10px)' },
          '60%': { transform: 'translateY(-5px)' },
        },
        'pulse-glow': {
          '0%': { boxShadow: '0 0 5px currentColor' },
          '100%': { boxShadow: '0 0 20px currentColor, 0 0 30px currentColor' },
        },
        'fadeInSlideUp': {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'typedjsBlink': {
          '0%': { opacity: '1' },
          '50%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      boxShadow: {
        'sm': '0 1px 2px 0 var(--shadow-color)',
        'md': '0 4px 6px -1px var(--shadow-color), 0 2px 4px -1px var(--shadow-color)',
        'lg': '0 10px 15px -3px var(--shadow-color), 0 4px 6px -2px var(--shadow-color)',
      },
    },
  },
  plugins: [],
}