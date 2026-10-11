import type { ToolExecution } from '../../lib/api/tools'

type ToolExecutionResultProps = {
  execution: ToolExecution
  onRunAnother: () => void
}

export function ToolExecutionResult({ execution, onRunAnother }: ToolExecutionResultProps) {
  const succeeded = execution.status === 'succeeded'
  return (
    <div className="execution-result" role="status">
      <p className={`execution-status ${succeeded ? 'is-success' : 'is-failure'}`}>
        <span aria-hidden="true">{succeeded ? 'OK' : 'FAILED'}</span>{' '}
        {succeeded ? 'Action completed' : 'Action failed'}
      </p>
      <p>{execution.message}</p>
      <dl className="proposal-details">
        <div>
          <dt>Device</dt>
          <dd>{execution.device_ref}</dd>
        </div>
        <div>
          <dt>Action</dt>
          <dd>{execution.tool_name}</dd>
        </div>
        <div>
          <dt>Recorded</dt>
          <dd>{new Date(execution.executed_at).toLocaleString()}</dd>
        </div>
      </dl>
      <button className="text-button" type="button" onClick={onRunAnother}>
        Prepare another action
      </button>
    </div>
  )
}
