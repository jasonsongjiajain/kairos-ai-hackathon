import type { ComponentProps, ReactNode } from 'react'
import { BookOpenText, CaretDown } from '@phosphor-icons/react'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { cn } from '@/lib/utils'

export type SourcesProps = ComponentProps<typeof Collapsible> & {
  count: number
  children: ReactNode
  label?: string
}

export function Sources({ className, count, children, label = 'Retrieved evidence', ...props }: SourcesProps) {
  return (
    <Collapsible className={cn('assistant-sources', className)} {...props}>
      <CollapsibleTrigger className="assistant-sources__trigger">
        <BookOpenText size={17} aria-hidden="true" />
        <span>{label}</span>
        <span className="assistant-sources__count">{count} {count === 1 ? 'source' : 'sources'}</span>
        <CaretDown size={16} aria-hidden="true" />
      </CollapsibleTrigger>
      <CollapsibleContent className="assistant-sources__content">{children}</CollapsibleContent>
    </Collapsible>
  )
}
