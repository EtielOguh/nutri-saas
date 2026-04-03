#!/bin/bash
# Script para setup do banco de dados PostgreSQL

set -e

echo \"🗄️  PostgreSQL Database Setup\"
echo \"=============================\"
echo \"\"

# Cores para output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

# Verificar se estamos no diretório correto
if [ ! -f \"requirements.txt\" ]; then
    echo -e \"${RED}❌ requirements.txt não encontrado!${NC}\"
    echo \"Execute este script a partir da raiz do projeto\"
    exit 1
fi

echo -e \"${YELLOW}1️⃣  Verificando dependências...${NC}\"
if ! command -v psql &> /dev/null; then
    echo -e \"${RED}❌ PostgreSQL CLI (psql) não está instalado${NC}\"
    exit 1
fi
echo -e \"${GREEN}✅ PostgreSQL instalado${NC}\"

echo \"\"
echo -e \"${YELLOW}2️⃣  Criando banco de dados...${NC}\"

# Valores padrão (podem ser sobrescritos por variáveis de ambiente)
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USERNAME:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}
DB_NAME=${DB_NAME:-nutri_saas}

# Criar banco se não existir
PGPASSWORD=\"$DB_PASSWORD\" psql -h \"$DB_HOST\" -p \"$DB_PORT\" -U \"$DB_USER\" -tc \"SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'\" | grep -q 1 || \
PGPASSWORD=\"$DB_PASSWORD\" psql -h \"$DB_HOST\" -p \"$DB_PORT\" -U \"$DB_USER\" -c \"CREATE DATABASE $DB_NAME;\"

echo -e \"${GREEN}✅ Banco criado: $DB_NAME${NC}\"

echo \"\"
echo -e \"${YELLOW}3️⃣  Rodando migrations (Alembic)...${NC}\"

# Verificar se Alembic está instalado
if ! python -c \"import alembic\" 2>/dev/null; then
    echo -e \"${RED}❌ Alembic não está instalado${NC}\"
    exit 1
fi

# Carregar variáveis de ambiente do .env
if [ -f \".env\" ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Rodar migrations
alembic upgrade head
echo -e \"${GREEN}✅ Migrations aplicadas${NC}\"

echo \"\"
echo -e \"${YELLOW}4️⃣  Verificando saúde do banco...${NC}\"
python -c \"
from sqlalchemy import create_engine, text
from core.config import settings

try:
    engine = create_engine(settings.get_database_url)
    with engine.connect() as conn:
        result = conn.execute(text('SELECT version()'))
        version = result.scalar()
        print(f'${GREEN}✅ Banco conectado:${NC}')
        print(f'   {version}')
except Exception as e:
    print(f'${RED}❌ Erro de conexão: {e}${NC}')
    exit(1)
\"

echo \"\"
echo -e \"${GREEN}✅ Setup concluído com sucesso!${NC}\"
echo \"\"
echo \"Próximos passos:\"
echo \"  1. Configure as variáveis de ambiente em .env\"
echo \"  2. Execute: python main.py\"
echo \"  3. Acesse: http://localhost:8000/api/docs\"
