from starlette.middleware.base import BaseHTTPMiddleware
from special.token import verify_token
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import JSONResponse

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude authentication and docs routes
        if request.url.path in ["/login", "/signUP", "/docs", "/openapi.json", "/redoc","/api/v1/signup/"]:
            return await call_next(request)

        # Get token from headers
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token format")
        
        # Extract actual token
        token = token.split(" ")[1]
        payload = verify_token(token)
        
        # Check token validity
        if "error" in payload:
            return JSONResponse(status_code=401, content={"detail": payload["error"]})
        
        # Attach user info to request state
        request.state.user = payload
        
        response = await call_next(request)
        return response