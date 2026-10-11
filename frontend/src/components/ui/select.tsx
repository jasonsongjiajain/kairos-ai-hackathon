import * as SelectPrimitive from '@radix-ui/react-select'
import { Check, CaretDown } from '@phosphor-icons/react'
import type { ReactNode } from 'react'
import { cn } from '../../lib/utils'

type SelectProps = {
  value: string
  onValueChange: (value: string) => void
  disabled?: boolean
  placeholder?: string
  children: ReactNode
  'aria-label'?: string
}

export function Select({ value, onValueChange, disabled, placeholder, children, ...props }: SelectProps) {
  return (
    <SelectPrimitive.Root value={value} onValueChange={onValueChange} disabled={disabled}>
      <SelectPrimitive.Trigger className="ui-select-trigger" {...props}>
        <SelectPrimitive.Value placeholder={placeholder} />
        <SelectPrimitive.Icon aria-hidden="true"><CaretDown size={16} /></SelectPrimitive.Icon>
      </SelectPrimitive.Trigger>
      <SelectPrimitive.Portal>
        <SelectPrimitive.Content className="ui-select-content" position="popper" sideOffset={4}>
          <SelectPrimitive.Viewport>{children}</SelectPrimitive.Viewport>
        </SelectPrimitive.Content>
      </SelectPrimitive.Portal>
    </SelectPrimitive.Root>
  )
}

export function SelectItem({ value, children }: { value: string; children: ReactNode }) {
  return (
    <SelectPrimitive.Item className={cn('ui-select-item')} value={value}>
      <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
      <SelectPrimitive.ItemIndicator className="ui-select-indicator"><Check size={15} /></SelectPrimitive.ItemIndicator>
    </SelectPrimitive.Item>
  )
}
