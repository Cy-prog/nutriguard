from pydantic_settings import BaseSettings
from pydantic import model_validator
from typing import Optional, List
import os

class Settings(BaseSettings):
    model_config = {"env_file": ".env", "case_sensitive": True}
    
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./nutriguard.db"
    
    JWT_SECRET: str = "dev-secret-do-not-use-in-prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    GEMINI_API_KEY: Optional[str] = None
    
    DEBUG: bool = False  # Added DEBUG flag for development/demo mode
    
    # Raw string from env var — will be parsed into a list in @property
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    RATE_LIMIT_ENABLED: bool = True

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        if self.ENVIRONMENT == "production":
            if (
                not self.JWT_SECRET 
                or self.JWT_SECRET == "dev-secret-do-not-use-in-prod" 
                or len(self.JWT_SECRET) < 32
            ):
                raise ValueError(
                    "CRITICAL SECURITY: In production, JWT_SECRET must be configured with a random string of at least 32 characters."
                )
        return self
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS into a proper list of origins.
        Supports comma-separated string or JSON array format.
        Never returns ['*'] when credentials are enabled — that's a CORS spec violation.
        """
        raw = self.CORS_ORIGINS.strip()
        if not raw:
            return ["http://localhost:5173"]
        
        # Handle JSON array format: ["https://a.com","https://b.com"]
        if raw.startswith("["):
            import json
            try:
                origins = json.loads(raw)
                if isinstance(origins, list):
                    return [o.strip() for o in origins if o.strip() and o.strip() != "*"]
            except (json.JSONDecodeError, TypeError):
                pass
        
        # Handle comma-separated format
        origins = [o.strip() for o in raw.split(",") if o.strip() and o.strip() != "*"]
        if not origins:
            origins = ["http://localhost:5173"]
        
        return origins

settings = Settings()
