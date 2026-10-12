"use client"

import { type ComponentProps, memo } from "react"
import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

type ShimmerProps = ComponentProps<"span"> & {
  duration?: number
}

const ShimmerComponent = ({ children, className, duration = 2, ...props }: ShimmerProps) => (
  <span className={cn("relative inline-block overflow-hidden", className)} {...props}>
    <motion.span
      aria-hidden="true"
      className="pointer-events-none absolute inset-0"
      style={{ background: "linear-gradient(90deg, transparent, var(--surface), transparent)" }}
      animate={{ translateX: ["-100%", "100%"] }}
      transition={{ repeat: Infinity, duration, ease: "linear" }}
    />
    <span className="relative">{children}</span>
  </span>
)

export const Shimmer = memo(ShimmerComponent)
