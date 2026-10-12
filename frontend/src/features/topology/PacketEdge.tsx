import { useEffect, useRef } from 'react'
import { BaseEdge, getStraightPath, type EdgeProps, type Edge } from '@xyflow/react'
import { gsap } from 'gsap'

type PacketData = { broken: boolean; paused: boolean; active: boolean }

export function PacketEdge({ id, sourceX, sourceY, targetX, targetY, style, data }: EdgeProps<Edge<PacketData>>) {
  const packets = useRef<SVGGElement>(null)
  const [path] = getStraightPath({ sourceX, sourceY, targetX, targetY })
  const active = data?.active ?? false
  const moving = !data?.paused && !data?.broken

  useEffect(() => {
    if (!moving || !packets.current) return
    const context = gsap.context(() => {
      const dots = packets.current!.querySelectorAll('circle')
      dots.forEach((dot, index) => {
        gsap.fromTo(dot,
          { x: sourceX, y: sourceY, opacity: 0 },
          { x: targetX, y: targetY, opacity: 1, duration: active ? 0.85 : 2.8,
            delay: index * (active ? 0.28 : 0.93), repeat: -1, ease: 'none' })
      })
    }, packets)
    return () => context.revert()
  }, [moving, active, sourceX, sourceY, targetX, targetY])

  return <>
    <BaseEdge id={id} path={path} style={{ ...style, stroke: active ? '#f3cb7a' : style?.stroke }} />
    {moving && <g ref={packets} aria-hidden="true" style={{ pointerEvents: 'none' }} fill={active ? '#f3cb7a' : '#63dcc2'}>
      {[0, 1, 2].map((index) => <circle key={index} r={active ? 3.5 : 2.5} opacity="0" />)}
    </g>}
  </>
}
