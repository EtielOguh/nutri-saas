#!/bin/bash
# Scripts úteis para gerenciamento de migrations com Alembic

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Nutri SaaS - Database Migration Scripts ===${NC}\n"

case "$1" in
  "init")
    echo -e "${YELLOW}Inicializando Alembic...${NC}"
    alembic init alembic
    ;;
  
  "revision")
    if [ -z "$2" ]; then
      echo "Uso: ./migrations.sh revision <nome_da_migracao>"
      exit 1
    fi
    echo -e "${YELLOW}Criando nova revisão: $2${NC}"
    alembic revision --autogenerate -m "$2"
    ;;
  
  "upgrade")
    if [ -z "$2" ]; then
      echo -e "${YELLOW}Atualizando para a última versão...${NC}"
      alembic upgrade head
    else
      echo -e "${YELLOW}Atualizando para: $2${NC}"
      alembic upgrade "$2"
    fi
    ;;
  
  "downgrade")
    if [ -z "$2" ]; then
      echo "Uso: ./migrations.sh downgrade <versão_anterior>"
      exit 1
    fi
    echo -e "${YELLOW}Revertendo para: $2${NC}"
    alembic downgrade "$2"
    ;;
  
  "history")
    echo -e "${BLUE}Histórico de migrations:${NC}"
    alembic history
    ;;
  
  "current")
    echo -e "${BLUE}Versão atual do banco:${NC}"
    alembic current
    ;;
  
  "heads")
    echo -e "${BLUE}Cabeças de branch:${NC}"
    alembic heads
    ;;
  
  "help")
    echo -e "${GREEN}Comandos disponíveis:${NC}"
    echo "  init              - Inicializa Alembic"
    echo "  revision <nome>   - Cria nova revisão de migração"
    echo "  upgrade [versão]  - Aplica migrations (padrão: head)"
    echo "  downgrade <versão> - Reverte para versão anterior"
    echo "  history           - Mostra histórico de migrations"
    echo "  current           - Mostra versão atual do banco"
    echo "  heads             - Mostra cabeças de branch"
    echo "  help              - Mostra esta ajuda"
    ;;
  
  *)
    echo "Comando não reconhecido. Use './migrations.sh help' para ver os comandos disponíveis."
    exit 1
    ;;
esac

echo -e "\n${GREEN}✓ Comando executado${NC}"
