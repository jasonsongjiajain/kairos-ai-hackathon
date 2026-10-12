import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeAll, describe, expect, it, vi } from 'vitest'
import { Dialog, DialogContent, DialogDescription, DialogTitle, DialogTrigger } from './dialog'
import { Select, SelectItem } from './select'

beforeAll(() => {
  HTMLElement.prototype.scrollIntoView = vi.fn()
})

describe('shared Radix primitives', () => {
  it('closes a dialog with Escape and restores focus to its trigger', async () => {
    const user = userEvent.setup()
    render(
      <Dialog>
        <DialogTrigger asChild><button type="button">Review action</button></DialogTrigger>
        <DialogContent aria-describedby="dialog-description">
          <DialogTitle>Confirm action</DialogTitle>
          <DialogDescription id="dialog-description">Review the pending change.</DialogDescription>
          <button type="button">Continue</button>
        </DialogContent>
      </Dialog>,
    )

    const trigger = screen.getByRole('button', { name: 'Review action' })
    await user.click(trigger)
    expect(screen.getByRole('dialog', { name: 'Confirm action' })).toBeInTheDocument()
    await user.keyboard('{Escape}')

    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    expect(trigger).toHaveFocus()
  })

  it('opens a select with the keyboard, selects an option, and returns focus to the trigger', async () => {
    const user = userEvent.setup()
    const onValueChange = vi.fn()
    render(
      <Select value="router-1" onValueChange={onValueChange} aria-label="Target device">
        <SelectItem value="router-1">Router 1</SelectItem>
        <SelectItem value="router-2">Router 2</SelectItem>
      </Select>,
    )

    const trigger = screen.getByRole('combobox', { name: 'Target device' })
    trigger.focus()
    await user.keyboard('{Enter}')
    expect(await screen.findByRole('option', { name: 'Router 2' })).toBeInTheDocument()
    await user.keyboard('{ArrowDown}{Enter}')

    expect(onValueChange).toHaveBeenCalledWith('router-2')
    await waitFor(() => expect(trigger).toHaveFocus())
  })

  it('closes an open select with Escape and restores trigger focus', async () => {
    const user = userEvent.setup()
    render(
      <Select value="router-1" onValueChange={vi.fn()} aria-label="Target device">
        <SelectItem value="router-1">Router 1</SelectItem>
      </Select>,
    )

    const trigger = screen.getByRole('combobox', { name: 'Target device' })
    trigger.focus()
    await user.keyboard('{Enter}')
    expect(await screen.findByRole('option', { name: 'Router 1' })).toBeInTheDocument()
    await user.keyboard('{Escape}')

    await waitFor(() => expect(screen.queryByRole('option', { name: 'Router 1' })).not.toBeInTheDocument())
    expect(trigger).toHaveFocus()
  })
})
