from contextvars import ContextVar

# This will hold the user object per request
user_ctx: ContextVar[dict] = ContextVar("user_ctx", default={})
