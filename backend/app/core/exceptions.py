class NexoraError(Exception):
    def __init__(self, detail: str, status_code: int = 500):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class SessionNotFound(NexoraError):
    def __init__(self, session_id: str):
        super().__init__(
            detail=f"Session not found: {session_id}",
            status_code=404,
        )


class ValidationError(NexoraError):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=400)


class ProviderError(NexoraError):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=502)