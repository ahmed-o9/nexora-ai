import { BrainCircuit } from 'lucide-react';

export function BrandMark({ compact = false }: { compact?: boolean }) {
  return (
    <div className="flex items-center gap-3" data-testid="brand-nexora">
      <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[hsl(var(--accent))] text-[hsl(var(--accent-foreground))] shadow-[0_8px_20px_rgba(220,235,115,.2)]">
        <BrainCircuit size={19} strokeWidth={2.2} aria-hidden="true" />
      </span>
      {!compact && (
        <span className="nexora-display text-[15px] font-bold tracking-[-0.03em] text-[hsl(var(--sidebar-foreground))]">
          NEXORA
        </span>
      )}
    </div>
  );
}