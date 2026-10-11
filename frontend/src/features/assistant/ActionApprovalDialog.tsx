import type { ReactNode } from 'react'
import { Button } from '../../components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogTitle,
} from '../../components/ui/dialog'

type ActionApprovalDialogProps = {
  title: string
  description: string
  confirmLabel: string
  busy?: boolean
  onConfirm: () => void
  onCancel: () => void
  children?: ReactNode
}

export function ActionApprovalDialog({
  title,
  description,
  confirmLabel,
  busy = false,
  onConfirm,
  onCancel,
  children,
}: ActionApprovalDialogProps) {
  return (
    <Dialog open onOpenChange={(open) => { if (!open) onCancel() }}>
      <DialogContent className="dialog" aria-describedby="approval-dialog-description">
        <DialogTitle id="approval-dialog-title">{title}</DialogTitle>
        <DialogDescription id="approval-dialog-description">{description}</DialogDescription>
        {children}
        <DialogFooter className="dialog-actions">
          <Button className="text-button" variant="quiet" type="button" onClick={onCancel} disabled={busy}>
            Cancel
          </Button>
          <Button
            className="process-button"
            type="button"
            onClick={onConfirm}
            disabled={busy}
          >
            {busy ? 'Executing...' : confirmLabel}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
