from fastapi import Request, HTTPException, status
from .config import settings
import time

# Very simple in-memory rate limiter for MVP demonstration.
# In a production environment with multiple instances, this MUST be backed by Redis.
# See Part 18 Requirements.

_rate_limit_store = {}
_LAST_CLEANUP = 0.0

def _extract_client_ip(request: Request) -> str:
    # 1. Check X-Forwarded-For header if behind a reverse proxy (e.g. Render, Cloudflare, ALB)
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        # First IP in comma-separated list is the client IP
        return forwarded.split(",")[0].strip()
    
    # 2. Direct socket client host
    if request.client and request.client.host:
        return request.client.host
        
    return "127.0.0.1"

def rate_limit_dependency(requests_per_minute: int = 60):
    def _rate_limit(request: Request):
        global _LAST_CLEANUP
        if not settings.RATE_LIMIT_ENABLED:
            return
            
        client_ip = _extract_client_ip(request)
        current_time = time.time()
        
        # Periodic cleanup of expired IP keys to prevent memory leak
        if current_time - _LAST_CLEANUP > 120:
            expired_keys = [
                ip for ip, timestamps in _rate_limit_store.items()
                if not timestamps or (current_time - timestamps[-1] >= 60)
            ]
            for ip in expired_keys:
                _rate_limit_store.pop(ip, None)
            _LAST_CLEANUP = current_time
        
        if client_ip not in _rate_limit_store:
            _rate_limit_store[client_ip] = []
            
        # Clear out requests older than 60 seconds
        _rate_limit_store[client_ip] = [t for t in _rate_limit_store[client_ip] if current_time - t < 60]
        
        if len(_rate_limit_store[client_ip]) >= requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
                detail="Too many requests. Please slow down."
            )
            
        _rate_limit_store[client_ip].append(current_time)
        
    return _rate_limit
