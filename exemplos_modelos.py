"""Exemplos de uso dos modelos SQLAlchemy."""

# ====== EXEMPLO 1: Criar um Nutricionista ======
def exemplo_criar_nutricionista():
    """Cria um novo nutricionista no sistema."""
    from models import Nutricionista
    from core.database import SessionLocal
    
    db = SessionLocal()
    
    nutricionista = Nutricionista(
        nome="Dra. Ana Silva",
        email="ana@nutricionista.com",
        senha_hash="hash_da_senha_segura_aqui"
    )
    
    db.add(nutricionista)
    db.commit()
    db.refresh(nutricionista)
    
    print(f"✅ Nutricionista criado: {nutricionista}")
    
    db.close()
    return nutricionista.id


# ====== EXEMPLO 2: Criar Configuração do Nutricionista ======
def exemplo_criar_configuracao(nutricionista_id):
    """Cria configurações personalizadas para um nutricionista."""
    from models import ConfiguracaoNutricionista
    from core.database import SessionLocal
    
    db = SessionLocal()
    
    config = ConfiguracaoNutricionista(
        nutricionista_id=nutricionista_id,
        logo_url="https://example.com/logo.png",
        cor_primaria="#FF6B35",
        valor_consulta=150.00,
        link_agendamento="https://calendly.com/ana"
    )
    
    db.add(config)
    db.commit()
    
    print(f"✅ Configuração criada para nutricionista {nutricionista_id}")
    
    db.close()


# ====== EXEMPLO 3: Criar Cliente ======
def exemplo_criar_cliente(nutricionista_id):
    """Cria um novo cliente para um nutricionista."""
    from models import Cliente
    from core.database import SessionLocal
    
    db = SessionLocal()
    
    cliente = Cliente(
        nutricionista_id=nutricionista_id,
        nome="João Santos",
        idade=42,
        altura=175.5,  # em centímetros
        objetivo="Emagrecimento e ganho de massa magra"
    )
    
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    
    print(f"✅ Cliente criado: {cliente}")
    
    db.close()
    return cliente.id


# ====== EXEMPLO 4: Registrar Medição ======
def exemplo_registrar_medicao(cliente_id):
    """Registra peso do cliente em uma data."""
    from models import Medicao
    from core.database import SessionLocal
    from datetime import datetime
    
    db = SessionLocal()
    
    medicao = Medicao(
        cliente_id=cliente_id,
        peso=92.5  # em kg
    )
    # data_medicao usa datetime.utcnow() por padrão
    
    db.add(medicao)
    db.commit()
    db.refresh(medicao)
    
    print(f"✅ Medição registrada: {medicao.peso}kg em {medicao.data_medicao}")
    
    db.close()


# ====== EXEMPLO 5: Múltiplas Medições ======
def exemplo_multiplas_medicoes(cliente_id):
    """Registra série de medições para acompanhamento."""
    from models import Medicao
    from core.database import SessionLocal
    from datetime import datetime, timedelta
    
    db = SessionLocal()
    
    pesos = [92.5, 91.8, 91.2, 90.5, 89.8]
    
    for i, peso in enumerate(pesos):
        medicao = Medicao(
            cliente_id=cliente_id,
            peso=peso,
            data_medicao=datetime.utcnow() - timedelta(days=(len(pesos)-i-1)*7)
        )
        db.add(medicao)
    
    db.commit()
    
    print(f"✅ {len(pesos)} medições registradas")
    
    db.close()


# ====== EXEMPLO 6: Adicionar Observação ======
def exemplo_adicionar_observacao(cliente_id):
    """Adiciona anotação do nutricionista sobre o cliente."""
    from models import Observacao
    from core.database import SessionLocal
    
    db = SessionLocal()
    
    obs = Observacao(
        cliente_id=cliente_id,
        texto="Cliente apresenta excelente adesão ao plano. "
              "Reduziu ingestão de carboidratos refinados em 80%. "
              "Próximo passo: aumentar frequência de exercícios."
    )
    
    db.add(obs)
    db.commit()
    
    print(f"✅ Observação adicionada para cliente {cliente_id}")
    
    db.close()


# ====== EXEMPLO 7: Criar Token de Acesso ======
def exemplo_criar_token_acesso(cliente_id):
    """Cria token único para acesso do cliente ao portal."""
    from models import TokenAcessoCliente
    from core.database import SessionLocal
    import secrets
    
    db = SessionLocal()
    
    token_unico = secrets.token_urlsafe(32)
    
    token = TokenAcessoCliente(
        cliente_id=cliente_id,
        token_unico=token_unico
    )
    
    db.add(token)
    db.commit()
    
    print(f"✅ Token criado: {token_unico[:20]}...")
    
    db.close()
    return token_unico


# ====== EXEMPLO 8: Adicionar Documento ======
def exemplo_adicionar_documento(cliente_id):
    """Adiciona referência a documento PDF (plano nutricional, relatório, etc)."""
    from models import DocumentoPDF
    from core.database import SessionLocal
    
    db = SessionLocal()
    
    doc = DocumentoPDF(
        cliente_id=cliente_id,
        url_pdf="https://storage.example.com/planos/cliente_123_plano_nutritivo.pdf"
    )
    
    db.add(doc)
    db.commit()
    
    print(f"✅ Documento adicionado for cliente {cliente_id}")
    
    db.close()


# ====== EXEMPLO 9: Buscar Nutricionista e Clientes ======
def exemplo_listar_clientes_nutricionista(nutricionista_id):
    """Lista todos os clientes de um nutricionista."""
    from models import Cliente
    from core.database import SessionLocal
    
    db = SessionLocal()
    
    clientes = db.query(Cliente).filter(
        Cliente.nutricionista_id == nutricionista_id
    ).all()
    
    print(f"✅ {len(clientes)} clientes encontrados:")
    for cliente in clientes:
        print(f"   - {cliente.nome} (ID: {cliente.id}, Idade: {cliente.idade})")
    
    db.close()


# ====== EXEMPLO 10: Histórico de Medições ======
def exemplo_historico_medicoes(cliente_id):
    """Obtém histórico de medições ordenado por data."""
    from models import Medicao
    from core.database import SessionLocal
    
    db = SessionLocal()
    
    medicoes = db.query(Medicao).filter(
        Medicao.cliente_id == cliente_id
    ).order_by(Medicao.data_medicao.desc()).all()
    
    print(f"✅ Histórico de {len(medicoes)} medições:")
    for med in medicoes:
        print(f"   {med.data_medicao.strftime('%d/%m/%Y')}: {med.peso}kg")
    
    db.close()


# ====== EXEMPLO 11: Autenticar por Token ======
def exemplo_autenticar_por_token(token_unico):
    """Encontra cliente pelo token e retorna dados."""
    from models import TokenAcessoCliente
    from core.database import SessionLocal
    
    db = SessionLocal()
    
    token_obj = db.query(TokenAcessoCliente).filter(
        TokenAcessoCliente.token_unico == token_unico
    ).first()
    
    if token_obj:
        cliente = token_obj.cliente
        print(f"✅ Cliente autenticado: {cliente.nome}")
        print(f"   Nutricionista: {cliente.nutricionista.nome}")
        print(f"   Objetivo: {cliente.objetivo}")
        return cliente
    else:
        print(f"❌ Token inválido")
        return None
    
    db.close()


# ====== EXEMPLO 12: Obter Todos os Dados de um Cliente ======
def exemplo_dados_completos_cliente(cliente_id):
    """Obtém todos os dados de um cliente usando relacionamentos."""
    from models import Cliente
    from core.database import SessionLocal
    
    db = SessionLocal()
    
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    if cliente:
        print(f"\n📋 Dados Completos do Cliente")
        print(f"═" * 50)
        print(f"Nome: {cliente.nome}")
        print(f"Idade: {cliente.idade} anos")
        print(f"Altura: {cliente.altura} cm")
        print(f"Objetivo: {cliente.objetivo}")
        print(f"Nutricionista: {cliente.nutricionista.nome}")
        
        print(f"\n📊 Medições ({len(cliente.medicoes)})")
        for med in cliente.medicoes[-3:]:  # Últimas 3
            print(f"   {med.data_medicao.strftime('%d/%m/%Y')}: {med.peso}kg")
        
        print(f"\n📝 Observações ({len(cliente.observacoes)})")
        for obs in cliente.observacoes[-2:]:  # Últimas 2
            print(f"   • {obs.texto[:60]}...")
        
        print(f"\n📄 Documentos ({len(cliente.documentos)})")
        for doc in cliente.documentos:
            print(f"   • {doc.url_pdf}")
        
        if cliente.token_acesso:
            print(f"\n🔑 Token de Acesso: {cliente.token_acesso.token_unico[:20]}...")
    
    db.close()


# ====== EXEMPLO 13: Query Avançada - Clientes com Peso Acima do Ideal ======
def exemplo_clientes_risco(nutricionista_id, peso_limite=90):
    """Encontra clientes com última medição acima do limite."""
    from models import Cliente, Medicao
    from core.database import SessionLocal
    from sqlalchemy import func, desc
    
    db = SessionLocal()
    
    # Sub-query: última medição por cliente
    subquery = db.query(
        Medicao.cliente_id,
        func.max(Medicao.data_medicao).label('ultima_data')
    ).group_by(Medicao.cliente_id).subquery()
    
    # Query principal
    clientes_risco = db.query(Cliente, Medicao).join(
        Medicao, Cliente.id == Medicao.cliente_id
    ).filter(
        Cliente.nutricionista_id == nutricionista_id,
        Medicao.peso > peso_limite
    ).all()
    
    print(f"✅ {len(clientes_risco)} cliente(s) acima do limite:")
    for cliente, medicao in clientes_risco:
        print(f"   - {cliente.nome}: {medicao.peso}kg")
    
    db.close()


# ====== MAIN: Executar Exemplos ======
if __name__ == "__main__":
    print("🧪 Exemplos de Uso dos Modelos SQLAlchemy\n")
    print("=" * 60 + "\n")
    
    # Descomente exemplos para testar:
    
    # 1. Criar nutricionista
    # nid = exemplo_criar_nutricionista()
    # exemplo_criar_configuracao(nid)
    
    # 2. Criar cliente
    # cid = exemplo_criar_cliente(nid)
    
    # 3. Registrar medições
    # exemplo_registrar_medicao(cid)
    # exemplo_multiplas_medicoes(cid)
    
    # 4. Adicionar observações
    # exemplo_adicionar_observacao(cid)
    
    # 5. Criar token
    # token = exemplo_criar_token_acesso(cid)
    
    # 6. Adicionar documento
    # exemplo_adicionar_documento(cid)
    
    # 7. Listar e buscar
    # exemplo_listar_clientes_nutricionista(nid)
    # exemplo_historico_medicoes(cid)
    
    # 8. Autenticar por token
    # exemplo_autenticar_por_token(token)
    
    # 9. Dados completos
    # exemplo_dados_completos_cliente(cid)
    
    # 10. Query avançada
    # exemplo_clientes_risco(nid, peso_limite=85)
    
    print("\n✅ Exemplos criados! Descomente no __main__ para testar.")
    print("\nPara usar em produção:")
    print("  1. Importe os modelos: from models import Cliente, Medicao, ...")
    print("  2. Use SessionLocal: db = SessionLocal()")
    print("  3. Faça queries: clientes = db.query(Cliente).all()")
