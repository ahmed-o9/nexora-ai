export interface VisualResult {
  title: string;
  image_url: string;
  thumbnail_url: string;
  source_url: string;
  source_name: string;
  query: string;
  width?: number | null;
  height?: number | null;
}

export interface TeachContent {
  explanation: string;
  example: string;
  analogy: string;
  key_points: string[];
  understanding_check: string | null;
  visuals: VisualResult[];
}

export interface TeachResponse {
  session_id: string;
  topic: string;
  level: string;
  mode: string;
  content: TeachContent;
  strategy: string;
  difficulty: number;
  tool_result: unknown;
}

export interface TeachRequest {
  question: string;
  mode: string;
  student_id: string;
  level: string | null;
}

const apiBase = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '');

function asString(value: unknown): string {
  return typeof value === 'string' ? value : '';
}

function normalizeVisual(value: unknown): VisualResult | null {
  if (!value || typeof value !== 'object') return null;
  const item = value as Record<string, unknown>;
  const title = asString(item.title);
  const imageUrl = asString(item.image_url);
  if (!title || !imageUrl) return null;
  return {
    title,
    image_url: imageUrl,
    thumbnail_url: asString(item.thumbnail_url),
    source_url: asString(item.source_url),
    source_name: asString(item.source_name),
    query: asString(item.query),
    width: typeof item.width === 'number' ? item.width : null,
    height: typeof item.height === 'number' ? item.height : null,
  };
}

function normalizeResponse(value: unknown): TeachResponse {
  if (!value || typeof value !== 'object') throw new Error('The teaching service returned an invalid response.');
  const item = value as Record<string, unknown>;
  const rawContent = item.content && typeof item.content === 'object'
    ? item.content as Record<string, unknown>
    : {};
  const rawPoints = Array.isArray(rawContent.key_points) ? rawContent.key_points : [];
  const rawVisuals = Array.isArray(rawContent.visuals) ? rawContent.visuals : [];
  return {
    session_id: asString(item.session_id),
    topic: asString(item.topic),
    level: asString(item.level),
    mode: asString(item.mode),
    content: {
      explanation: asString(rawContent.explanation),
      example: asString(rawContent.example),
      analogy: asString(rawContent.analogy),
      key_points: rawPoints.filter((point): point is string => typeof point === 'string'),
      understanding_check: rawContent.understanding_check === null
        ? null
        : asString(rawContent.understanding_check),
      visuals: rawVisuals.map(normalizeVisual).filter((visual): visual is VisualResult => visual !== null),
    },
    strategy: asString(item.strategy),
    difficulty: typeof item.difficulty === 'number' && Number.isFinite(item.difficulty)
      ? item.difficulty
      : 0,
    tool_result: item.tool_result,
  };
}

export async function teachQuestion(
  request: TeachRequest,
  signal?: AbortSignal,
): Promise<TeachResponse> {
  let response: Response;
  try {
    response = await fetch(`${apiBase}/teach`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(request),
      signal,
    });
  } catch {
    throw new Error('Nexora is offline or could not reach the teaching service.');
  }

  if (!response.ok) {
    throw new Error('Nexora could not complete that lesson right now.');
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new Error('Nexora returned an unreadable teaching response.');
  }
  return normalizeResponse(payload);
}

