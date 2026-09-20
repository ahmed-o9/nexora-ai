import { Plus, SlidersHorizontal } from 'lucide-react';

interface ControlsBarProps {
  mode: string;
  level: string | null;
  onModeChange: (mode: string) => void;
  onLevelChange: (level: string | null) => void;
  onNewSession: () => void;
  disabled?: boolean;
}

const modes = [
  { value: 'learn', label: 'Learn' },
  { value: 'exam', label: 'Exam' },
  { value: 'interview', label: 'Interview' },
  { value: 'socratic', label: 'Socratic' },
  { value: 'research', label: 'Research' },
  { value: 'quiz', label: 'Quiz' },
  { value: 'revise', label: 'Revise' },
];

const levels = [
  { value: '', label: 'Adaptive level' },
  { value: 'beginner', label: 'Foundations' },
  { value: 'intermediate', label: 'Working knowledge' },
  { value: 'advanced', label: 'Deep systems' },
];

export function ControlsBar({
  mode,
  level,
  onModeChange,
  onLevelChange,
  onNewSession,
  disabled,
}: ControlsBarProps) {
  return (
    <div className="flex flex-col gap-3 border-b border-[hsl(var(--border))] pb-5 sm:flex-row sm:items-center sm:justify-between" data-testid="controls-teaching">
      <div className="flex items-center gap-2">
        <SlidersHorizontal size={15} className="text-[hsl(var(--muted-foreground))]" aria-hidden="true" />
        <span className="nexora-mono text-[10px] font-medium uppercase tracking-[.15em] text-[hsl(var(--muted-foreground))]">Teaching mode</span>
        <div className="ml-1 hidden rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--card))] p-1 sm:flex">
          {modes.map((item) => (
            <button
              key={item.value}
              type="button"
              disabled={disabled}
              onClick={() => onModeChange(item.value)}
              className={`rounded-md px-3 py-1.5 text-xs font-semibold transition-colors ${mode === item.value ? 'bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))]' : 'text-[hsl(var(--muted-foreground))] hover:bg-[hsl(var(--muted))] hover:text-[hsl(var(--foreground))]'}`}
              data-testid={`button-mode-${item.value}`}
              aria-pressed={mode === item.value}
            >
              {item.label}
            </button>
          ))}
        </div>
        <select
          id="mode-select"
          value={mode}
          disabled={disabled}
          onChange={(event) => onModeChange(event.target.value)}
          className="ml-1 h-9 min-w-0 flex-1 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--card))] px-3 text-xs font-semibold text-[hsl(var(--foreground))] sm:hidden"
          aria-label="Teaching mode"
          data-testid="select-mode"
        >
          {modes.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}
        </select>
      </div>
      <div className="flex items-center gap-2">
        <label htmlFor="level-select" className="nexora-mono text-[10px] font-medium uppercase tracking-[.15em] text-[hsl(var(--muted-foreground))]">Level</label>
        <select
          id="level-select"
          value={level ?? ''}
          disabled={disabled}
          onChange={(event) => onLevelChange(event.target.value || null)}
          className="h-9 max-w-[170px] rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--card))] px-3 text-xs font-semibold text-[hsl(var(--foreground))] shadow-sm"
          data-testid="select-level"
        >
          {levels.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}
        </select>
        <button
          type="button"
          onClick={onNewSession}
          className="ml-1 inline-flex h-9 items-center gap-1.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--card))] px-3 text-xs font-semibold text-[hsl(var(--foreground))] transition-colors hover:bg-[hsl(var(--muted))]"
          data-testid="button-new-session"
        >
          <Plus size={14} aria-hidden="true" />
          <span className="hidden sm:inline">New session</span>
          <span className="sm:hidden">New</span>
        </button>
      </div>
    </div>
  );
}