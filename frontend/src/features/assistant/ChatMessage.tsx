import type { ReactNode } from 'react'
import { motion, useReducedMotion } from 'framer-motion'
import { arrive } from '../../lib/motion'

type ChatMessageProps = {
  role: 'user' | 'assistant'
  label: string
  children: ReactNode
}

export function ChatMessage({ role, label, children }: ChatMessageProps) {
  const reducedMotion = Boolean(useReducedMotion())
  return (
    <motion.li className={`chat-message chat-message-${role}`} variants={arrive} initial="hidden" animate="visible" custom={reducedMotion}>
      <p className="chat-role">{label}</p>
      <div className="chat-body">{children}</div>
    </motion.li>
  )
}
