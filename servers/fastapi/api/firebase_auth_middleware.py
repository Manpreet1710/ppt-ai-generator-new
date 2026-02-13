from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import time
import logging
from firebase_admin import auth
from context.user_context import user_ctx
logger = logging.getLogger(__name__)

class FirebaseAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_paths = [
            "/api/v1/user-config",
            "/api/v1/ppt/presentation/all",
            "/api/v1/ppt/template-management/summary",
            "/api/v1/subscription-routes/plans",
            "/health",
            "/api/v1/subscription-routes/webhook",
            "/api/v1/subscription-routes/reconciliation"
        ]

        # Skip auth for OPTIONS requests and excluded paths (with prefix matching)
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Check if path starts with any excluded path
        for excluded in excluded_paths:
            if request.url.path.startswith(excluded):
                return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.warning("No Authorization header found")
            return JSONResponse({"error": "Unauthorized - No token"}, status_code=401)

        

        if not auth_header.startswith("Bearer "):
            return JSONResponse({"error": "Unauthorized - Malformed token"}, status_code=401)

        parts = auth_header.split(" ")
        if len(parts) != 2:
            return JSONResponse({"error": "Unauthorized - Invalid token format"}, status_code=401)

        token = parts[1].strip()

        if not token:
            return JSONResponse({"error": "Unauthorized - Empty token"}, status_code=401)

        try:
            start_time = time.time()

            decoded_token = auth.verify_id_token(token)
            user_ctx.set(decoded_token)
            end_time = time.time()
            logger.info(f"Time taken to verify token: {end_time - start_time:.4f} seconds")

            uid = decoded_token["uid"]
            email = decoded_token.get("email", "unknown@example.com")
            request.state.user = decoded_token
            doc_name = "user_usage"
            llm = "gemini"
           
            body = {}
            if request.headers.get("content-type") == "application/json":
                try:
                    body = await request.json()
                    request.state.body = body  # preserve for downstream
                except Exception:
                    body = {}

            plan = decoded_token.get("plan")
            model_name = body.get("model_name", "gemini-2.0-flash")
            if not plan or plan.lower()=="free":
                 if model_name!="gemini-2.0-flash":
                     return JSONResponse(
                        {"error": f"Model '{model_name}' not supported. Please upgrade to use this model."},
                        status_code=403,
                    )

            return await call_next(request)

        except Exception as e:
            logger.warning(f"Token verification failed: {str(e)}")
            return JSONResponse({"error": "Invalid or expired token"}, status_code=401)