import { ArrowUpRight, Braces, GitBranch, Network } from 'lucide-react';

interface EmptyStateProps {
  onSuggestion: (question: string) => void;
}

const suggestions = [
  { label: 'Trace a request', text: 'Trace an HTTP request from browser to database, including the failure points.', icon: GitBranch },
  { label: 'Understand queues', text: 'Explain message queues by comparing delivery guarantees and backpressure.', icon: Network },
  { label: 'Review a system', text: 'Help me reason about the tradeoffs in a URL shortener design.', icon: Braces },
];

export function EmptyState({ onSuggestion }: EmptyStateProps) {
  return (
    <section className="nexora-enter mx-auto w-full max-w-[800px] py-8 sm:py-16" aria-labelledby="empty-title" data-testid="empty-state">
      <div className="relative overflow-hidden rounded-[1.5rem] border border-[hsl(var(--border))] bg-[hsl(var(--card))] px-6 py-10 shadow-[var(--shadow-soft)] sm:px-12 sm:py-14">
        <div className="nexora-dotted-grid pointer-events-none absolute right-[-2rem] top-[-2rem] h-40 w-40 opacity-40" aria-hidden="true" />
        <div className="relative max-w-[590px]">
          <div className="mb-7 flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-[hsl(var(--primary))] text-[hsl(var(--accent))]">
              <span className="h-2.5 w-2.5 rounded-full bg-[hsl(var(--accent))] shadow-[0_0_0_5px_rgba(220,235,115,.16)]" />
            </span>
            <span className="nexora-mono text-[10px] uppercase tracking-[.17em] text-[hsl(var(--muted-foreground))]">Instrument ready</span>
          </div>
          <h1 id="empty-title" className="nexora-display max-w-[570px] text-4xl font-semibold leading-[1.02] tracking-[-.05em] text-[hsl(var(--foreground))] sm:text-6xl">
            Ask better questions.<br />
            <span className="text-[hsl(var(--muted-foreground))]">See the system.</span>
          </h1>
          <p className="mt-6 max-w-[530px] text-[15px] leading-7 text-[hsl(var(--muted-foreground))]">
            Nexora helps you build a mental model before it gives you an answer. Start with a system, a failure, or a decision you want to understand.
          </p>
          <div className="mt-9 grid gap-2 sm:grid-cols-3" aria-label="Suggested lessons">
            {suggestions.map(({ label, text, icon: Icon }) => (
              <button
                key={label}
                type="button"
                onClick={() => onSuggestion(text)}
                className="group flex min-h-[102px] flex-col justify-between rounded-xl border border-[hsl(var(--border))] bg-[hsl(var(--background))] p-3.5 text-left transition-transform hover:-translate-y-0.5 hover:border-[hsl(var(--foreground))]"
                data-testid={`button-suggestion-${label.toLowerCase().replaceAll(' ', '-')}`}
              >
                <Icon size={16} className="text-[hsl(var(--primary))]" aria-hidden="true" />
                <span className="flex items-center justify-between gap-2 text-xs font-semibold text-[hsl(var(--foreground))]">
                  {label}
                  <ArrowUpRight size={13} className="opacity-0 transition-opacity group-hover:opacity-100" aria-hidden="true" />
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>
      <p className="mt-5 text-center nexora-mono text-[10px] uppercase tracking-[.14em] text-[hsl(var(--muted-foreground))]">A precise learning instrument for systems thinking</p>
    </section>
  );
}