from fastapi import Request
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exception:
            return JSONResponse(content={"detail": http_exception.detail}, status_code=http_exception.status_code)
        except Exception as e:
            return JSONResponse(content={"detail": "internal server error"}, status_code=500)
