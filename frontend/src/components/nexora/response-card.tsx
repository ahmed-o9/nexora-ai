import { Check, CheckCircle2, Lightbulb, ListChecks, Route, Sparkles } from 'lucide-react';
import type { ReactNode } from 'react';
import type { TeachResponse } from '@/lib/nexora-api';
import { VisualCard } from './visual-card';

function textBlocks(text: string): ReactNode {
  if (!text) return null;
  return text.split(/\n{2,}/).map((block, index) => (
    <p key={`${block.slice(0, 12)}-${index}`} className="whitespace-pre-wrap leading-7">
      {block}
    </p>
  ));
}

function safeToolResult(value: unknown): string | null {
  if (value === null || value === undefined) return null;
  if (typeof value === 'string') return value;
  try {
    const serialized = JSON.stringify(value, null, 2);
    return serialized.length > 3600 ? `${serialized.slice(0, 3600)}\n…` : serialized;
  } catch {
    return 'A verified result was received from the teaching tool.';
  }
}

function Section({
  title,
  eyebrow,
  icon: Icon,
  children,
}: {
  title: string;
  eyebrow: string;
  icon: typeof Lightbulb;
  children: ReactNode;
}) {
  return (
    <section className="border-t border-[hsl(var(--border))] pt-5" data-testid={`section-${eyebrow.toLowerCase().replaceAll(' ', '-')}`}>
      <div className="mb-3 flex items-center gap-2">
        <Icon size={15} className="text-[hsl(var(--primary))]" aria-hidden="true" />
        <span className="nexora-mono text-[10px] font-medium uppercase tracking-[.15em] text-[hsl(var(--muted-foreground))]">{eyebrow}</span>
      </div>
      <h3 className="nexora-display mb-2 text-lg font-semibold tracking-[-.025em] text-[hsl(var(--foreground))]">{title}</h3>
      <div className="text-[14px] text-[hsl(var(--muted-foreground))]">{children}</div>
    </section>
  );
}

export function ResponseCard({ response }: { response: TeachResponse }) {
  const difficulty = Math.min(5, Math.max(0, Math.round(response.difficulty)));
  const verified = safeToolResult(response.tool_result);
  return (
    <article className="nexora-enter overflow-hidden rounded-2xl border border-[hsl(var(--border))] bg-[hsl(var(--card))] shadow-[var(--shadow-card)]" data-testid="card-teaching-response">
      <header className="border-b border-[hsl(var(--border))] bg-[hsl(var(--primary))] px-5 py-5 text-[hsl(var(--primary-foreground))] sm:px-7">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="nexora-mono mb-2 text-[10px] uppercase tracking-[.17em] text-[hsl(var(--accent))]">{response.mode || 'Teaching response'}</p>
            <h2 className="nexora-display text-2xl font-semibold tracking-[-.04em] sm:text-3xl">{response.topic || 'Systems lesson'}</h2>
          </div>
          <div className="rounded-lg border border-white/15 bg-white/5 px-3 py-2 text-right">
            <p className="nexora-mono text-[9px] uppercase tracking-[.12em] text-white/60">Difficulty</p>
            <div className="mt-1 flex gap-1" aria-label={`Difficulty ${difficulty} of 5`}>
              {[0, 1, 2, 3, 4].map((level) => <span key={level} className={`h-1.5 w-5 rounded-full ${level < difficulty ? 'bg-[hsl(var(--accent))]' : 'bg-white/20'}`} />)}
            </div>
          </div>
        </div>
        <div className="mt-5 flex flex-wrap gap-x-5 gap-y-2 text-[11px] text-white/65">
          {response.level && <span className="nexora-mono">LEVEL / {response.level}</span>}
          {response.session_id && <span className="nexora-mono">SESSION / {response.session_id.slice(0, 12)}</span>}
        </div>
      </header>

      <div className="space-y-7 px-5 py-6 sm:px-7 sm:py-8">
        <Section title="The mental model" eyebrow="Explanation" icon={Lightbulb}>
          {textBlocks(response.content.explanation)}
        </Section>
        <div className="grid gap-7 md:grid-cols-2">
          <Section title="Worked example" eyebrow="Example" icon={Route}>
            {textBlocks(response.content.example)}
          </Section>
          <Section title="A useful analogy" eyebrow="Analogy" icon={Sparkles}>
            {textBlocks(response.content.analogy)}
          </Section>
        </div>
        {response.content.key_points.length > 0 && (
          <Section title="Keep these in working memory" eyebrow="Key points" icon={ListChecks}>
            <ul className="space-y-2.5">
              {response.content.key_points.map((point, index) => (
                <li key={`${point.slice(0, 15)}-${index}`} className="flex gap-3">
                  <Check size={15} className="mt-1 shrink-0 text-[hsl(var(--primary))]" aria-hidden="true" />
                  <span>{point}</span>
                </li>
              ))}
            </ul>
          </Section>
        )}
        {response.content.understanding_check && (
          <section className="rounded-xl border border-[hsl(var(--primary))]/15 bg-[hsl(var(--secondary))] p-4" data-testid="section-understanding-check">
            <p className="nexora-mono mb-2 text-[10px] font-medium uppercase tracking-[.15em] text-[hsl(var(--primary))]">Check your understanding</p>
            <p className="text-sm leading-6 text-[hsl(var(--foreground))]">{response.content.understanding_check}</p>
          </section>
        )}
        {response.content.visuals.length > 0 && (
          <section className="border-t border-[hsl(var(--border))] pt-5" data-testid="section-visuals">
            <div className="mb-4 flex items-center justify-between gap-3">
              <div>
                <p className="nexora-mono text-[10px] font-medium uppercase tracking-[.15em] text-[hsl(var(--muted-foreground))]">Visual references</p>
                <h3 className="nexora-display mt-1 text-lg font-semibold tracking-[-.025em]">See the shape of it</h3>
              </div>
              <span className="nexora-mono text-[10px] text-[hsl(var(--muted-foreground))]">{response.content.visuals.length.toString().padStart(2, '0')} SOURCES</span>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              {response.content.visuals.map((visual, index) => <VisualCard key={`${visual.image_url}-${index}`} visual={visual} index={index} />)}
            </div>
          </section>
        )}
        {response.strategy && (
          <section className="rounded-xl border border-dashed border-[hsl(var(--border))] p-4" data-testid="section-strategy">
            <p className="nexora-mono mb-2 text-[10px] font-medium uppercase tracking-[.15em] text-[hsl(var(--muted-foreground))]">Teaching strategy</p>
            <p className="text-sm leading-6 text-[hsl(var(--muted-foreground))]">{response.strategy}</p>
          </section>
        )}
        {verified && (
          <section className="rounded-xl border border-[hsl(var(--accent))]/60 bg-[hsl(var(--accent))]/15 p-4" data-testid="verified-result">
            <div className="flex items-start gap-3">
              <CheckCircle2 size={18} className="mt-0.5 shrink-0 text-[hsl(var(--primary))]" aria-hidden="true" />
              <div className="min-w-0">
                <p className="nexora-mono text-[10px] font-medium uppercase tracking-[.15em] text-[hsl(var(--primary))]">Verified result</p>
                <p className="mt-1 text-xs leading-5 text-[hsl(var(--muted-foreground))]">This result was returned by a teaching tool and kept separate from the explanation.</p>
                <pre className="mt-3 max-h-64 overflow-auto whitespace-pre-wrap break-words rounded-lg bg-[rgba(34,45,77,.07)] p-3 nexora-mono text-[11px] leading-5 text-[hsl(var(--foreground))]">{verified}</pre>
              </div>
            </div>
          </section>
        )}
      </div>
    </article>
  );
}