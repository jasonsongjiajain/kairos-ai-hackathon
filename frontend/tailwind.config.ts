import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        canvas: 'var(--canvas)',
        surface: 'var(--surface)',
        elevated: 'var(--elevated)',
        text: { primary: 'var(--text-primary)', secondary: 'var(--text-secondary)' },
        border: 'var(--border)',
        focus: 'var(--focus)',
        success: { DEFAULT: 'var(--success)', surface: 'var(--success-surface)' },
        warning: { DEFAULT: 'var(--warning)', surface: 'var(--warning-surface)' },
        error: { DEFAULT: 'var(--error)', surface: 'var(--error-surface)' },
      },
      borderRadius: {
        sm: 'var(--radius-small)',
        DEFAULT: 'var(--radius-control)',
        lg: 'var(--radius-panel)',
      },
      transitionDuration: { DEFAULT: '120ms' },
      transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.22, 1, 0.36, 1)' },
    },
  },
  plugins: [],
} satisfies Config
