import { forwardRef, type ButtonHTMLAttributes } from 'react'
import { cn } from '../../lib/utils'

type ButtonVariant =
  | 'primary'
  | 'default'
  | 'secondary'
  | 'outline'
  | 'quiet'
  | 'ghost'
  | 'danger'
  | 'destructive'

type ButtonSize = 'default' | 'sm' | 'lg' | 'icon'

export type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant
  size?: ButtonSize
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'default', ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        'ui-button',
        `ui-button-${variant}`,
        size !== 'default' && `ui-button-size-${size}`,
        className,
      )}
      {...props}
    />
  ),
)
Button.displayName = 'Button'
