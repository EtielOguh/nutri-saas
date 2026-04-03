# Dashboard - Quick Start

## Endpoint

```
GET /nutricionistas/{nutricionista_id}/dashboard
```

## Resposta

```json
{
  "nutricionista_id": 1,
  "nome": "Dra. Maria",
  "email": "maria@exemplo.com",
  "metricas": {
    "total_clientes": 15,
    "total_medicoes": 87,
    "media_peso": 72.5,
    "num_clientes_ativos": 12
  },
  "clientes_recentes": [...],
  "configuracao": {...}
}
```

## Uso Rápido

### Python
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8000/nutricionistas/1/dashboard")
    dashboard = response.json()
    print(f"Total: {dashboard['metricas']['total_clientes']} clientes")
```

### JavaScript
```javascript
const dashboard = await fetch('/nutricionistas/1/dashboard').then(r => r.json());
console.log(`Total: ${dashboard.metricas.total_clientes} clientes`);
```

### cURL
```bash
curl http://localhost:8000/nutricionistas/1/dashboard | jq '.metricas'
```

## Métricas

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `total_clientes` | int | Total de clientes |
| `total_medicoes` | int | Total de medições registradas |
| `media_peso` | float | Média de peso (últimas medições) |
| `num_clientes_ativos` | int | Clientes com medição no último mês |

## Performance

- ✅ Queries otimizadas (50-300ms)
- ✅ Sem N+1 queries
- ✅ Suporta até 10K clientes
- ✅ JSON formatado

## Testes

```bash
# Rodar testes
pytest test_dashboard.py -v

# Coverage
pytest test_dashboard.py --cov=services.nutricionista_service
```

## Arquivos Relacionados

- `services/nutricionista_service.py` - Implementação da query
- `api/routes/nutricionista.py` - Endpoint REST
- `schemas/nutricionista.py` - Schema de resposta
- `test_dashboard.py` - Testes unitários
- `DASHBOARD_DOCUMENTATION.md` - Documentação completa
