import type { Config } from 'tailwindcss'
import animate from 'tailwindcss-animate'

export default {
    darkMode: ['class'],
    corePlugins: { preflight: false },
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
  	extend: {
  		colors: {
  			canvas: 'var(--canvas)',
  			surface: 'var(--surface)',
  			elevated: 'var(--elevated)',
  			text: {
  				primary: 'var(--text-primary)',
  				secondary: 'var(--text-secondary)'
  			},
  			border: 'var(--border)',
  			focus: 'var(--focus)',
  			success: {
  				DEFAULT: 'var(--success)',
  				surface: 'var(--success-surface)'
  			},
  			warning: {
  				DEFAULT: 'var(--warning)',
  				surface: 'var(--warning-surface)'
  			},
  			error: {
  				DEFAULT: 'var(--error)',
  				surface: 'var(--error-surface)'
  			},
  			background: 'var(--background)',
  			foreground: 'var(--foreground)',
  			card: {
  				DEFAULT: 'var(--card)',
  				foreground: 'var(--card-foreground)'
  			},
  			popover: {
  				DEFAULT: 'var(--popover)',
  				foreground: 'var(--popover-foreground)'
  			},
  			primary: {
  				DEFAULT: 'var(--primary)',
  				foreground: 'var(--primary-foreground)'
  			},
  			secondary: {
  				DEFAULT: 'var(--secondary)',
  				foreground: 'var(--secondary-foreground)'
  			},
  			muted: {
  				DEFAULT: 'var(--muted)',
  				foreground: 'var(--muted-foreground)'
  			},
  			accent: {
  				DEFAULT: 'var(--accent)',
  				foreground: 'var(--accent-foreground)'
  			},
  			destructive: {
  				DEFAULT: 'var(--destructive)',
  				foreground: 'var(--destructive-foreground)'
  			},
  			input: 'var(--input)',
  			ring: 'var(--ring)'
  		},
  		borderRadius: {
  			sm: 'var(--radius-small)',
  			DEFAULT: 'var(--radius-control)',
  			lg: 'var(--radius-panel)'
  		},
  		transitionDuration: {
  			DEFAULT: '120ms'
  		},
  		transitionTimingFunction: {
  			DEFAULT: 'cubic-bezier(0.22, 1, 0.36, 1)'
  		},
  		keyframes: {
  			'accordion-down': {
  				from: {
  					height: '0'
  				},
  				to: {
  					height: 'var(--radix-accordion-content-height)'
  				}
  			},
  			'accordion-up': {
  				from: {
  					height: 'var(--radix-accordion-content-height)'
  				},
  				to: {
  					height: '0'
  				}
  			}
  		},
  		animation: {
  			'accordion-down': 'accordion-down 0.2s ease-out',
  			'accordion-up': 'accordion-up 0.2s ease-out'
  		}
  	}
  },
  plugins: [animate],
} satisfies Config
