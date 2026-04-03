"""Arquivo principal - Inicialização da aplicação FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from core.config import settings
from core.database import engine, init_db, close_db
from api.routes import health, cliente, cliente_direto, tmb, public, nutricionista, pdf, auth

# Inicialização da aplicação
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão de rotas
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(public.router)
app.include_router(tmb.router)
app.include_router(cliente.router)
app.include_router(cliente_direto.router_cliente_direto)
app.include_router(nutricionista.router)
app.include_router(pdf.router)

# Servir arquivos estáticos (uploads)
uploads_dir = Path("uploads")
if uploads_dir.exists():
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Eventos de inicialização
@app.on_event("startup")
async def startup_event() -> None:
    """Executado ao iniciar a aplicação."""
    db_url = settings.get_database_url
    print(f"✅ Iniciando {settings.APP_NAME} (v{settings.APP_VERSION})")
    print(f"📊 Banco de dados: {db_url.split('@')[1] if '@' in db_url else db_url}")
    print(f"🏠 Servidor: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/api/docs")
    # Descomente a linha abaixo para criar as tabelas automaticamente no primeiro setup
    # init_db()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Executado ao desligar a aplicação."""
    close_db()
    print(f"🛑 {settings.APP_NAME} desligada")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
