import type { ComponentProps, ReactNode } from 'react'
import { CaretDown } from '@phosphor-icons/react'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { cn } from '@/lib/utils'

type ReasoningProps = ComponentProps<typeof Collapsible> & {
  active?: boolean
  title?: string
  children: ReactNode
}

export function Reasoning({ className, active = false, title, children, ...props }: ReasoningProps) {
  return (
    <Collapsible className={cn('assistant-reasoning', className)} {...props}>
      <CollapsibleTrigger className="assistant-reasoning__trigger">
        <span className={cn('assistant-reasoning__mark', active && 'is-active')} aria-hidden="true" />
        <span>{title ?? (active ? 'Checking ticket evidence and guidance' : 'Evidence checks')}</span>
        <CaretDown size={16} aria-hidden="true" />
      </CollapsibleTrigger>
      <CollapsibleContent className="assistant-reasoning__content">{children}</CollapsibleContent>
    </Collapsible>
  )
}
