import type { Transition, Variants } from 'framer-motion'

// Seconds, matching Framer Motion. CSS control feedback uses 120ms.
export const motionDuration = { control: 0.12, state: 0.22, sequence: 0.4 } as const
export const motionEase = [0.22, 1, 0.36, 1] as const

export function prefersReducedMotion(): boolean {
  return typeof window !== 'undefined'
    && typeof window.matchMedia === 'function'
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

export function transitionFor(
  reducedMotion: boolean,
  duration: number = motionDuration.state,
): Transition {
  return reducedMotion
    ? { type: 'tween', duration: 0, delay: 0 }
    : { type: 'tween', duration, ease: motionEase }
}

// Pass useReducedMotion() through custom; hidden also resolves to final state.
export const arrive: Variants = {
  hidden: (reducedMotion: boolean = prefersReducedMotion()) => ({
    opacity: reducedMotion ? 1 : 0, y: reducedMotion ? 0 : 8,
  }),
  visible: (reducedMotion: boolean = prefersReducedMotion()) => ({
    opacity: 1, y: 0, transition: transitionFor(reducedMotion),
  }),
}

export const reveal: Variants = {
  hidden: (reducedMotion: boolean = prefersReducedMotion()) => ({
    opacity: reducedMotion ? 1 : 0,
  }),
  visible: (reducedMotion: boolean = prefersReducedMotion()) => ({
    opacity: 1, transition: transitionFor(reducedMotion, motionDuration.sequence),
  }),
}

export const settle: Variants = {
  hidden: (reducedMotion: boolean = prefersReducedMotion()) => ({
    opacity: reducedMotion ? 1 : 0, scale: reducedMotion ? 1 : 0.98,
  }),
  visible: (reducedMotion: boolean = prefersReducedMotion()) => ({
    opacity: 1, scale: 1, transition: transitionFor(reducedMotion),
  }),
}

// Runnable boundary check: npx vite-node src/lib/motion.ts --check-motion
if (typeof process !== 'undefined' && process.argv.includes('--check-motion')) {
  const immediate = transitionFor(true, motionDuration.sequence)
  if (!('duration' in immediate) || immediate.duration !== 0 || immediate.delay !== 0) {
    throw new Error('Reduced motion must have no duration or delay')
  }
  for (const variants of [arrive, reveal, settle]) {
    const hidden = variants.hidden
    const visible = variants.visible
    if (typeof hidden !== 'function' || typeof visible !== 'function') {
      throw new Error('Motion variants must resolve the motion preference')
    }
    const start = hidden(true, {}, {})
    const end = visible(true, {}, {})
    if (typeof start === 'string' || typeof end === 'string') {
      throw new Error('Motion variants must return targets')
    }
    if (start.opacity !== end.opacity || start.y !== end.y || start.scale !== end.scale) {
      throw new Error('Reduced motion must start in the final state')
    }
  }
  if (prefersReducedMotion()) throw new Error('Absent window must default to false')
  const originalWindow = Object.getOwnPropertyDescriptor(globalThis, 'window')
  try {
    Object.defineProperty(globalThis, 'window', { configurable: true, value: {} })
    if (prefersReducedMotion()) throw new Error('Absent matchMedia must default to false')
    for (const matches of [true, false]) {
      Object.defineProperty(globalThis, 'window', {
        configurable: true,
        value: { matchMedia: (query: string) => {
          if (query !== '(prefers-reduced-motion: reduce)') throw new Error('Wrong media query')
          return { matches }
        } },
      })
      if (prefersReducedMotion() !== matches) throw new Error('Motion preference ignored')
    }
  } finally {
    if (originalWindow) Object.defineProperty(globalThis, 'window', originalWindow)
    else Reflect.deleteProperty(globalThis, 'window')
  }
}
