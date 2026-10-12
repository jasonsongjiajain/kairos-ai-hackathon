import type { HTMLAttributes } from 'react'
import { cn } from '../../lib/utils'

type BadgeVariant =
  | 'default'
  | 'secondary'
  | 'outline'
  | 'success'
  | 'warning'
  | 'error'
  | 'destructive'

export function Badge({
  className,
  variant = 'default',
  ...props
}: HTMLAttributes<HTMLSpanElement> & { variant?: BadgeVariant }) {
  return (
    <span
      className={cn('ui-badge', variant !== 'default' && `ui-badge-${variant}`, className)}
      {...props}
    />
  )
}
