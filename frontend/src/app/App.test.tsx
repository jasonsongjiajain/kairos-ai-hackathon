import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import App from './App'

describe('App', () => {
  it('renders the named field operations shell', () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: 'Field Force Incident Assistant', level: 1 })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Ready for the next job', level: 2 })).toBeInTheDocument()
  })
})
