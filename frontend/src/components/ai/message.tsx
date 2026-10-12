"use client"

import type { HTMLAttributes } from "react"
import { cn } from "@/lib/utils"

export type MessageProps = HTMLAttributes<HTMLDivElement> & {
  from: "user" | "assistant" | "system"
}

export function Message({ className, from, ...props }: MessageProps) {
  return (
    <div
      className={cn(
        "group flex w-full flex-col gap-2",
        from === "user" && "is-user ml-auto justify-end",
        from === "assistant" && "is-assistant",
        className,
      )}
      {...props}
    />
  )
}

export type MessageContentProps = HTMLAttributes<HTMLDivElement>

export function MessageContent({ className, ...props }: MessageContentProps) {
  return (
    <div
      className={cn("flex w-fit max-w-full min-w-0 flex-col gap-2 overflow-hidden text-sm", className)}
      {...props}
    />
  )
}
