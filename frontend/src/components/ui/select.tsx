import * as SelectPrimitive from '@radix-ui/react-select'
import { Check, CaretDown } from '@phosphor-icons/react'
import type { ComponentPropsWithoutRef, ReactNode } from 'react'
import { cn } from '../../lib/utils'

type SelectProps = Omit<ComponentPropsWithoutRef<typeof SelectPrimitive.Trigger>, 'value' | 'onChange'> & {
  value: string
  onValueChange: (value: string) => void
  placeholder?: string
  children: ReactNode
}

export function Select({ value, onValueChange, disabled, placeholder, children, className, ...props }: SelectProps) {
  return (
    <SelectPrimitive.Root value={value} onValueChange={onValueChange} disabled={disabled}>
      <SelectPrimitive.Trigger className={cn('ui-select-trigger', className)} {...props}>
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

export function SelectItem({ value, children, className, ...props }: ComponentPropsWithoutRef<typeof SelectPrimitive.Item>) {
  return (
    <SelectPrimitive.Item className={cn('ui-select-item', className)} value={value} {...props}>
      <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
      <SelectPrimitive.ItemIndicator className="ui-select-indicator"><Check size={15} /></SelectPrimitive.ItemIndicator>
    </SelectPrimitive.Item>
  )
}
