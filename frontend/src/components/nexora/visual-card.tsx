import { ExternalLink, ImageOff, Maximize2, X } from 'lucide-react';
import { useEffect, useState } from 'react';
import type { VisualResult } from '@/lib/nexora-api';

export function VisualCard({ visual, index }: { visual: VisualResult; index: number }) {
  const [isOpen, setIsOpen] = useState(false);
  const [imageFailed, setImageFailed] = useState(false);

  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setIsOpen(false);
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  const thumbnail = visual.thumbnail_url || visual.image_url;
  return (
    <>
      <article className="overflow-hidden rounded-xl border border-[hsl(var(--border))] bg-[hsl(var(--background))]" data-testid={`card-visual-${index}`}>
        <button
          type="button"
          onClick={() => !imageFailed && setIsOpen(true)}
          className="group relative block aspect-[16/9] w-full overflow-hidden bg-[hsl(var(--muted))] text-left"
          aria-label={`Open larger view of ${visual.title}`}
          disabled={imageFailed}
          data-testid={`button-open-visual-${index}`}
        >
          {imageFailed ? (
            <span className="flex h-full flex-col items-center justify-center gap-2 text-[hsl(var(--muted-foreground))]">
              <ImageOff size={20} aria-hidden="true" />
              <span className="text-xs">Visual unavailable</span>
            </span>
          ) : (
            <>
              <img
                src={thumbnail}
                alt={visual.title}
                loading="lazy"
                className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-[1.03]"
                onError={() => setImageFailed(true)}
              />
              <span className="absolute right-2 top-2 rounded-md bg-[hsl(var(--primary))] p-1.5 text-[hsl(var(--primary-foreground))] opacity-0 transition-opacity group-hover:opacity-100">
                <Maximize2 size={14} aria-hidden="true" />
              </span>
            </>
          )}
        </button>
        <div className="flex items-start justify-between gap-3 p-3.5">
          <div className="min-w-0">
            <h3 className="truncate text-sm font-semibold text-[hsl(var(--foreground))]">{visual.title}</h3>
            <p className="mt-1 truncate nexora-mono text-[10px] uppercase tracking-[.08em] text-[hsl(var(--muted-foreground))]">
              {visual.source_name || visual.query || 'Source visual'}
            </p>
          </div>
          {visual.source_url && (
            <a
              href={visual.source_url}
              target="_blank"
              rel="noreferrer"
              aria-label={`Open source for ${visual.title}`}
              className="shrink-0 rounded-md p-1 text-[hsl(var(--muted-foreground))] hover:bg-[hsl(var(--muted))] hover:text-[hsl(var(--foreground))]"
              data-testid={`link-visual-source-${index}`}
            >
              <ExternalLink size={14} aria-hidden="true" />
            </a>
          )}
        </div>
      </article>
      {isOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label={`${visual.title} enlarged`}
          className="fixed inset-0 z-50 flex items-center justify-center bg-[rgba(18,24,44,.82)] p-4"
          onClick={() => setIsOpen(false)}
          data-testid={`dialog-visual-${index}`}
        >
          <div className="relative max-h-[90vh] max-w-[min(1000px,94vw)] overflow-hidden rounded-2xl bg-[hsl(var(--card))] p-2 shadow-2xl" onClick={(event) => event.stopPropagation()}>
            <img src={visual.image_url} alt={visual.title} className="max-h-[78vh] max-w-full rounded-xl object-contain" />
            <div className="flex items-center justify-between gap-4 px-2 pb-1 pt-3">
              <p className="text-sm font-semibold text-[hsl(var(--foreground))]">{visual.title}</p>
              <button type="button" onClick={() => setIsOpen(false)} className="rounded-lg p-2 hover:bg-[hsl(var(--muted))]" aria-label="Close visual" data-testid={`button-close-visual-${index}`}>
                <X size={17} aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}