"""Configuração da aplicação com base em variáveis de ambiente."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # ===== INFORMAÇÕES DA APLICAÇÃO =====
    APP_NAME: str = "Nutri SaaS API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production

    # ===== SERVIDOR =====
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ===== BANCO DE DADOS - PostgreSQL =====
    # Configuração via URL completa (prioridade)
    DATABASE_URL: Optional[str] = None
    
    # OU configuração via componentes (fallback)
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "nutri_saas"
    DB_DRIVER: str = "psycopg2"  # psycopg2, asyncpg, etc.
    
    # Connection pool (para SaaS com múltiplos acessos)
    DB_POOL_SIZE: int = 10  # Número de conexões a manter no pool
    DB_MAX_OVERFLOW: int = 20  # Conexões adicionais quando pool está cheio
    DB_POOL_RECYCLE: int = 3600  # Reciclar conexões a cada 1 hora
    DB_ECHO: bool = False  # Log SQL em desenvolvimento

    # ===== JWT =====
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ===== CORS =====
    ALLOWED_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def get_database_url(self) -> str:
        """Constrói a URL do banco a partir da configuração."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        # Construir URL a partir dos componentes
        return (
            f"postgresql+{self.DB_DRIVER}://"
            f"{self.DB_USERNAME}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
