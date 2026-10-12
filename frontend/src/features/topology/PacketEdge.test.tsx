import { render, cleanup } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { Position } from '@xyflow/react'
import { PacketEdge } from './PacketEdge'

const animation = vi.hoisted(() => ({ fromTo: vi.fn(), revert: vi.fn() }))
vi.mock('gsap', () => ({ gsap: { fromTo: animation.fromTo, context: (callback: () => void) => { callback(); return { revert: animation.revert } } } }))
vi.mock('@xyflow/react', () => ({ BaseEdge: ({ path }: { path: string }) => <path d={path} />, getStraightPath: () => ['M 0,0 L 100,100'], Position: { Bottom: 'bottom', Top: 'top' } }))

afterEach(() => { cleanup(); vi.clearAllMocks() })
const props = { id: 'link', source: 'a', target: 'b', sourceX: 0, sourceY: 0, targetX: 100, targetY: 100, sourcePosition: Position.Bottom, targetPosition: Position.Top } as const

describe('packet animation lifecycle', () => {
  it('never sends packets on interrupted or paused links', () => {
    // Positions are consumed by React Flow, which is replaced by the SVG test boundary.
    const { rerender } = render(<svg><PacketEdge {...props} data={{ broken: true, paused: false, active: false }} /></svg>)
    expect(animation.fromTo).not.toHaveBeenCalled()
    rerender(<svg><PacketEdge {...props} data={{ broken: false, paused: true, active: true }} /></svg>)
    expect(animation.fromTo).not.toHaveBeenCalled()
  })
  it('cancels running packets when paused and cleans up on unmount', () => {
    const { rerender, unmount } = render(<svg><PacketEdge {...props} data={{ broken: false, paused: false, active: false }} /></svg>)
    expect(animation.fromTo).toHaveBeenCalledTimes(3)
    rerender(<svg><PacketEdge {...props} data={{ broken: false, paused: true, active: false }} /></svg>)
    expect(animation.revert).toHaveBeenCalledTimes(1)
    rerender(<svg><PacketEdge {...props} data={{ broken: false, paused: false, active: true }} /></svg>)
    expect(animation.fromTo).toHaveBeenLastCalledWith(expect.anything(), expect.anything(), expect.objectContaining({ duration: 0.85 }))
    unmount()
    expect(animation.revert).toHaveBeenCalledTimes(2)
  })
})
