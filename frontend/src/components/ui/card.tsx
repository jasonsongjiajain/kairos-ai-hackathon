import { forwardRef, type HTMLAttributes } from 'react'
import { cn } from '../../lib/utils'

export const Card = forwardRef<HTMLElement, HTMLAttributes<HTMLElement>>(({ className, ...props }, ref) => (
  <section ref={ref} className={cn('ui-card', className)} {...props} />
))
Card.displayName = 'Card'

export function CardHeader({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <header className={cn('ui-card-header', className)} {...props} />
}

export function CardContent({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('ui-card-content', className)} {...props} />
}
