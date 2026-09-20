import { BookOpen, CircleHelp, Clock3, Compass, PanelLeft, RotateCcw, ShieldCheck, WifiOff } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import type { TeachRequest, TeachResponse } from '@/lib/nexora-api';
import { teachQuestion } from '@/lib/nexora-api';
import { BrandMark } from './brand-mark';
import { Composer } from './composer';
import { ControlsBar } from './controls-bar';
import { EmptyState } from './empty-state';
import { ResponseCard } from './response-card';

type Message = {
  id: string;
  role: 'user' | 'assistant';
  text?: string;
  request?: TeachRequest;
  status?: 'pending' | 'complete' | 'error';
  response?: TeachResponse;
  error?: string;
};

const navItems = [
  { label: 'Teaching workspace', icon: Compass, active: true },
  { label: 'Sessions', icon: Clock3, active: false },
  { label: 'Progress', icon: BookOpen, active: false },
];

function createId() {
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) return crypto.randomUUID();
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function LoadingResponse() {
  return (
    <div className="nexora-enter rounded-2xl border border-[hsl(var(--border))] bg-[hsl(var(--card))] p-6 shadow-[var(--shadow-card)]" role="status" aria-label="Nexora is thinking" data-testid="status-teaching-loading">
      <div className="flex items-center gap-3">
        <BrandMark compact />
        <div>
          <p className="text-sm font-semibold text-[hsl(var(--foreground))]">Building a mental model</p>
          <p className="nexora-mono mt-1 text-[10px] uppercase tracking-[.12em] text-[hsl(var(--muted-foreground))]">Mapping the system · checking assumptions</p>
        </div>
      </div>
      <div className="mt-7 space-y-3">
        <div className="nexora-pulse h-3 w-[92%] rounded bg-[hsl(var(--muted))]" />
        <div className="nexora-pulse h-3 w-[77%] rounded bg-[hsl(var(--muted))]" />
        <div className="nexora-pulse h-3 w-[65%] rounded bg-[hsl(var(--muted))]" />
      </div>
    </div>
  );
}

export function TeachingWorkspace() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [composer, setComposer] = useState('');
  const [mode, setMode] = useState('learn');
  const [level, setLevel] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorBanner, setErrorBanner] = useState<string | null>(null);
  const [failedAssistantId, setFailedAssistantId] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const studentIdRef = useRef('nexora-browser-learner');

  useEffect(() => {
    const reducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    messagesEndRef.current?.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth' });
  }, [messages]);

  const sendQuestion = async (question: string, retryAssistantId?: string) => {
    const trimmed = question.trim();
    if (!trimmed || isLoading) return;

    const request: TeachRequest = {
      question: trimmed,
      mode,
      student_id: studentIdRef.current,
      level,
    };
    const assistantId = retryAssistantId ?? createId();
    if (retryAssistantId) {
      setMessages((current) => current.map((message) => (
        message.id === retryAssistantId
          ? { ...message, status: 'pending', error: undefined, response: undefined }
          : message
      )));
    } else {
      setMessages((current) => [
        ...current,
        { id: createId(), role: 'user', text: trimmed, request },
        { id: assistantId, role: 'assistant', status: 'pending', request },
      ]);
    }
    setComposer('');
    setErrorBanner(null);
    setFailedAssistantId(null);
    setIsLoading(true);

    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    try {
      const response = await teachQuestion(request, controller.signal);
      setSessionId(response.session_id || null);
      setMessages((current) => current.map((message) => (
        message.id === assistantId
          ? { ...message, status: 'complete', response }
          : message
      )));
    } catch (error) {
      if (controller.signal.aborted) return;
      const message = error instanceof Error ? error.message : 'Nexora could not reach the teaching service.';
      setMessages((current) => current.map((item) => (
        item.id === assistantId
          ? { ...item, status: 'error', error: message }
          : item
      )));
      setErrorBanner(message);
      setFailedAssistantId(assistantId);
    } finally {
      if (abortRef.current === controller) {
        abortRef.current = null;
        setIsLoading(false);
      }
    }
  };

  const newSession = () => {
    abortRef.current?.abort();
    abortRef.current = null;
    setMessages([]);
    setComposer('');
    setMode('learn');
    setLevel(null);
    setSessionId(null);
    setErrorBanner(null);
    setFailedAssistantId(null);
    setIsLoading(false);
  };

  const retryFailed = () => {
    if (!failedAssistantId) return;
    const failed = messages.find((message) => message.id === failedAssistantId);
    if (failed?.request) void sendQuestion(failed.request.question, failedAssistantId);
  };

  return (
    <div className="nexora-app nexora-grain flex min-h-[100dvh]">
      <aside className="nexora-sidebar hidden w-[248px] shrink-0 flex-col border-r border-[hsl(var(--sidebar-border))] px-4 py-5 text-[hsl(var(--sidebar-foreground))] md:flex" aria-label="Primary navigation">
        <div className="px-2"><BrandMark /></div>
        <div className="mt-12 px-2">
          <p className="nexora-mono mb-3 text-[9px] uppercase tracking-[.17em] text-white/35">Workspace</p>
          <nav className="space-y-1">
            {navItems.map(({ label, icon: Icon, active }) => (
              <button
                key={label}
                type="button"
                disabled={!active}
                className={`flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-sm transition-colors ${active ? 'bg-[hsl(var(--sidebar-accent))] font-semibold text-[hsl(var(--sidebar-accent-foreground))]' : 'cursor-not-allowed text-white/35'}`}
                title={active ? label : `${label} is not available in this workspace`}
                data-testid={`button-nav-${label.toLowerCase().replaceAll(' ', '-')}`}
              >
                <Icon size={16} strokeWidth={active ? 2.2 : 1.7} aria-hidden="true" />
                {label}
                {!active && <span className="ml-auto nexora-mono text-[8px] uppercase tracking-[.1em]">Soon</span>}
              </button>
            ))}
          </nav>
        </div>
        <div className="mt-auto rounded-xl border border-white/10 bg-white/[.035] p-3.5">
          <div className="flex items-start gap-2.5">
            <ShieldCheck size={16} className="mt-0.5 text-[hsl(var(--accent))]" aria-hidden="true" />
            <div>
              <p className="text-xs font-semibold text-white/80">Learn the machinery</p>
              <p className="mt-1 text-[11px] leading-5 text-white/40">Answers are structured to help you reason, not memorize.</p>
            </div>
          </div>
        </div>
        <div className="mt-4 flex items-center justify-between px-2 text-white/35">
          <span className="nexora-mono text-[9px] uppercase tracking-[.14em]">Nexora AI</span>
          <CircleHelp size={14} aria-hidden="true" />
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-[72px] shrink-0 items-center justify-between border-b border-[hsl(var(--border))] bg-[hsl(var(--background))]/80 px-4 backdrop-blur-sm sm:px-7" aria-label="Workspace header">
          <div className="flex items-center gap-3">
            <div className="md:hidden"><BrandMark compact /></div>
            <PanelLeft size={16} className="hidden text-[hsl(var(--muted-foreground))] md:block" aria-hidden="true" />
            <div>
              <p className="nexora-mono text-[10px] uppercase tracking-[.15em] text-[hsl(var(--muted-foreground))]">Teaching workspace</p>
              <p className="mt-0.5 text-xs font-semibold text-[hsl(var(--foreground))]">{sessionId ? `Session ${sessionId.slice(0, 12)}` : 'New learning session'}</p>
            </div>
          </div>
          <button type="button" onClick={newSession} className="inline-flex items-center gap-2 rounded-lg px-2.5 py-2 text-xs font-semibold text-[hsl(var(--muted-foreground))] transition-colors hover:bg-[hsl(var(--muted))] hover:text-[hsl(var(--foreground))]" data-testid="button-header-new-session">
            <RotateCcw size={14} aria-hidden="true" />
            <span className="hidden sm:inline">Reset workspace</span>
          </button>
        </header>

        <main className="flex min-h-0 flex-1 flex-col">
          <div className="mx-auto w-full max-w-[1120px] flex-1 px-4 pb-3 pt-5 sm:px-7 sm:pt-7">
            <ControlsBar
              mode={mode}
              level={level}
              onModeChange={setMode}
              onLevelChange={setLevel}
              onNewSession={newSession}
              disabled={isLoading}
            />
            {errorBanner && (
              <div className="mt-5 flex items-center justify-between gap-3 rounded-xl border border-[hsl(var(--destructive))]/30 bg-[hsl(var(--destructive))]/8 px-4 py-3" role="alert" data-testid="status-connection-error">
                <div className="flex min-w-0 items-center gap-3">
                  <WifiOff size={16} className="shrink-0 text-[hsl(var(--destructive))]" aria-hidden="true" />
                  <p className="truncate text-xs font-medium text-[hsl(var(--foreground))]">{errorBanner}</p>
                </div>
                <button type="button" onClick={retryFailed} disabled={!failedAssistantId || isLoading} className="shrink-0 rounded-md px-2.5 py-1.5 text-xs font-semibold text-[hsl(var(--destructive))] hover:bg-[hsl(var(--destructive))]/10] disabled:opacity-40" data-testid="button-retry-teaching">Retry</button>
              </div>
            )}
            {messages.length === 0 ? (
              <EmptyState onSuggestion={(question) => void sendQuestion(question)} />
            ) : (
              <section className="mx-auto max-w-[800px] space-y-6 py-7 sm:py-10" aria-label="Teaching conversation" data-testid="conversation">
                {messages.map((message) => (
                  <div key={message.id} className="nexora-enter">
                    {message.role === 'user' ? (
                      <div className="ml-auto max-w-[85%] rounded-2xl rounded-br-md bg-[hsl(var(--primary))] px-4 py-3.5 text-sm leading-6 text-[hsl(var(--primary-foreground))] shadow-sm" data-testid={`message-user-${message.id}`}>
                        {message.text}
                      </div>
                    ) : message.status === 'pending' ? (
                      <LoadingResponse />
                    ) : message.status === 'error' ? (
                      <div className="rounded-2xl border border-[hsl(var(--destructive))]/25 bg-[hsl(var(--card))] p-5" data-testid={`message-error-${message.id}`}>
                        <div className="flex items-start gap-3">
                          <WifiOff size={17} className="mt-0.5 shrink-0 text-[hsl(var(--destructive))]" aria-hidden="true" />
                          <div>
                            <p className="text-sm font-semibold text-[hsl(var(--foreground))]">The lesson could not load.</p>
                            <p className="mt-1 text-xs leading-5 text-[hsl(var(--muted-foreground))]">Check the connection to Nexora, then try the same question again.</p>
                            <button type="button" onClick={() => message.request && void sendQuestion(message.request.question, message.id)} className="mt-3 inline-flex items-center gap-1.5 text-xs font-semibold text-[hsl(var(--primary))] hover:underline" data-testid={`button-retry-message-${message.id}`}>
                              <RotateCcw size={13} aria-hidden="true" /> Retry question
                            </button>
                          </div>
                        </div>
                      </div>
                    ) : message.response ? (
                      <ResponseCard response={message.response} />
                    ) : null}
                  </div>
                ))}
                <div ref={messagesEndRef} aria-hidden="true" />
              </section>
            )}
          </div>
          <div className="sticky bottom-0 border-t border-[hsl(var(--border))] bg-[hsl(var(--background))]/92 px-4 pb-4 pt-3 backdrop-blur-md sm:px-7 sm:pb-6">
            <div className="mx-auto max-w-[800px]">
              <Composer value={composer} disabled={isLoading} onChange={setComposer} onSubmit={() => void sendQuestion(composer)} />
              <p className="mt-2 text-center nexora-mono text-[9px] uppercase tracking-[.12em] text-[hsl(var(--muted-foreground))]">Nexora can make mistakes · verify critical implementation details</p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}