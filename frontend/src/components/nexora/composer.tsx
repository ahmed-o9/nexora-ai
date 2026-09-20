import { ArrowUp, CornerDownLeft, LoaderCircle } from 'lucide-react';
import type { FormEvent, KeyboardEvent } from 'react';

interface ComposerProps {
  value: string;
  disabled: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
}

export function Composer({ value, disabled, onChange, onSubmit }: ComposerProps) {
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit();
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      onSubmit();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-2xl border border-[hsl(var(--border))] bg-[hsl(var(--card))] p-2 shadow-[var(--shadow-soft)]" data-testid="form-teaching-composer">
      <label htmlFor="teaching-question" className="sr-only">Your systems question</label>
      <textarea
        id="teaching-question"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        rows={2}
        placeholder="Ask about a system, tradeoff, or failure mode…"
        className="max-h-40 min-h-[72px] w-full resize-none border-0 bg-transparent px-3 py-2 text-[15px] leading-6 text-[hsl(var(--foreground))] outline-none placeholder:text-[hsl(var(--muted-foreground))] disabled:opacity-60"
        data-testid="textarea-teaching-question"
      />
      <div className="flex items-center justify-between border-t border-[hsl(var(--border))] px-2 pt-2">
        <span className="hidden items-center gap-1.5 text-[11px] text-[hsl(var(--muted-foreground))] sm:flex">
          <CornerDownLeft size={13} aria-hidden="true" />
          Enter to teach · Shift + Enter for a new line
        </span>
        <span className="sm:hidden" />
        <button
          type="submit"
          disabled={disabled || !value.trim()}
          className="inline-flex h-9 items-center gap-2 rounded-lg bg-[hsl(var(--primary))] px-3.5 text-xs font-semibold text-[hsl(var(--primary-foreground))] transition-transform hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-40"
          data-testid="button-submit-question"
        >
          {disabled ? <LoaderCircle size={15} className="animate-spin" aria-hidden="true" /> : <ArrowUp size={15} aria-hidden="true" />}
          <span>{disabled ? 'Thinking' : 'Teach me'}</span>
        </button>
      </div>
    </form>
  );
}