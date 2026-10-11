import type { ReactNode } from 'react'

type ChatMessageProps = {
  role: 'user' | 'assistant'
  label: string
  children: ReactNode
}

export function ChatMessage({ role, label, children }: ChatMessageProps) {
  return (
    <li className={`chat-message chat-message-${role}`}>
      <p className="chat-role">{label}</p>
      <div className="chat-body">{children}</div>
    </li>
  )
}
