"""Serviço de operações com Nutricionista."""
import os
import uuid
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from fastapi import UploadFile

from models.nutricionista import Nutricionista, ConfiguracaoNutricionista
from schemas.nutricionista import NutricionistaCreate, ConfiguracaoNutricionistaUpdate
from services.base import BaseService


# Configurações de upload
UPLOAD_DIR = Path("uploads")
LOGOS_DIR = UPLOAD_DIR / "logos"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


class NutricionistaService(BaseService[Nutricionista, NutricionistaCreate]):
    """
    Serviço para operações com Nutricionista.
    
    Operações disponíveis:
    - CRUD básico (herdado de BaseService)
    - Upload de logo
    - Gerenciamento de configurações
    """

    def __init__(self, db: Session):
        """Inicializa o serviço com o modelo Nutricionista."""
        super().__init__(model=Nutricionista, db=db)

    def get_by_email(self, email: str) -> Optional[Nutricionista]:
        """
        Busca nutricionista por email.
        
        Args:
            email: Email do nutricionista
            
        Returns:
            Nutricionista ou None se não encontrado
        """
        return self.db.query(Nutricionista).filter(
            Nutricionista.email == email
        ).first()

    def upload_logo(
        self,
        nutricionista_id: int,
        file: UploadFile,
    ) -> Tuple[str, str, int]:
        """
        Faz upload de uma logo para um nutricionista.
        
        Args:
            nutricionista_id: ID do nutricionista
            file: Arquivo da logo
            
        Returns:
            Tuple[logo_url, logo_path, file_size]: URL da logo, caminho relativo e tamanho
            
        Raises:
            ValueError: Se arquivo inválido ou nutricionista não existe
            IOError: Se houver erro ao salvar arquivo
        """
        # Validar que nutricionista existe
        nutricionista = self.get_by_id(nutricionista_id)
        if not nutricionista:
            raise ValueError(f"Nutricionista com ID {nutricionista_id} não encontrado")

        # Validar extensão do arquivo
        if not file.filename:
            raise ValueError("Nome do arquivo não fornecido")

        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Tipo de arquivo não permitido. Formatos aceitos: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Criar diretório se não existir
        LOGOS_DIR.mkdir(parents=True, exist_ok=True)

        # Gerar nome único para o arquivo
        # Formato: {nutricionista_id}_{uuid_curto}.{extensão}
        unique_id = uuid.uuid4().hex[:8]
        new_filename = f"{nutricionista_id}_{unique_id}{file_ext}"
        file_path = LOGOS_DIR / new_filename

        # Ler, validar tamanho e salvar arquivo
        file_content = file.file.read()
        file_size = len(file_content)

        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"Arquivo muito grande. Tamanho máximo: 5MB, fornecido: {file_size / 1024 / 1024:.2f}MB")

        if file_size == 0:
            raise ValueError("Arquivo vazio")

        # Salvar arquivo
        try:
            with open(file_path, "wb") as f:
                f.write(file_content)
        except IOError as e:
            raise IOError(f"Erro ao salvar arquivo: {str(e)}")

        # Gerar URL relativa
        logo_url = f"/uploads/logos/{new_filename}"
        logo_path = str(file_path)

        # Atualizar ou criar configuração do nutricionista
        config = self.db.query(ConfiguracaoNutricionista).filter(
            ConfiguracaoNutricionista.nutricionista_id == nutricionista_id
        ).first()

        if config:
            # Remover logo antiga se existir
            if config.logo_url:
                old_file_path = Path(config.logo_url.lstrip("/"))
                if old_file_path.exists():
                    try:
                        old_file_path.unlink()
                    except OSError:
                        pass  # Ignorar erro ao deletar arquivo antigo

            config.logo_url = logo_url
        else:
            config = ConfiguracaoNutricionista(
                nutricionista_id=nutricionista_id,
                logo_url=logo_url,
            )
            self.db.add(config)

        self.db.commit()
        self.db.refresh(config)

        return logo_url, logo_path, file_size

    def delete_logo(self, nutricionista_id: int) -> bool:
        """
        Remove a logo de um nutricionista.
        
        Args:
            nutricionista_id: ID do nutricionista
            
        Returns:
            bool: True se logo foi removida, False caso contrário
        """
        config = self.db.query(ConfiguracaoNutricionista).filter(
            ConfiguracaoNutricionista.nutricionista_id == nutricionista_id
        ).first()

        if not config or not config.logo_url:
            return False

        # Remover arquivo físico
        file_path = Path(config.logo_url.lstrip("/"))
        if file_path.exists():
            try:
                file_path.unlink()
            except OSError:
                pass  # Ignorar erro ao deletar arquivo

        # Atualizar banco de dados
        config.logo_url = None
        self.db.commit()

        return True

    def get_configuracao(self, nutricionista_id: int) -> Optional[ConfiguracaoNutricionista]:
        """
        Obtém configurações de um nutricionista.
        
        Args:
            nutricionista_id: ID do nutricionista
            
        Returns:
            ConfiguracaoNutricionista ou None
        """
        return self.db.query(ConfiguracaoNutricionista).filter(
            ConfiguracaoNutricionista.nutricionista_id == nutricionista_id
        ).first()

    def update_configuracao(
        self,
        nutricionista_id: int,
        config_data: ConfiguracaoNutricionistaUpdate,
    ) -> ConfiguracaoNutricionista:
        """
        Atualiza configurações de um nutricionista.
        
        Args:
            nutricionista_id: ID do nutricionista
            config_data: Dados para atualizar
            
        Returns:
            ConfiguracaoNutricionista atualizada
            
        Raises:
            ValueError: Se nutricionista não existe
        """
        config = self.db.query(ConfiguracaoNutricionista).filter(
            ConfiguracaoNutricionista.nutricionista_id == nutricionista_id
        ).first()

        if not config:
            # Verificar que nutricionista existe
            nutricionista = self.get_by_id(nutricionista_id)
            if not nutricionista:
                raise ValueError(f"Nutricionista com ID {nutricionista_id} não encontrado")

            # Criar com valores padrão (valor_consulta será 0.0 por padrão)
            config = ConfiguracaoNutricionista(nutricionista_id=nutricionista_id)
            self.db.add(config)

        # Atualizar campos fornecidos
        update_data = config_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(config, key, value)

        self.db.commit()
        self.db.refresh(config)

        return config

    def get_dashboard_data(self, nutricionista_id: int) -> Dict[str, Any]:
        """
        Obtém dados agregados do dashboard para um nutricionista.
        
        Usa queries eficientes com SQLAlchemy para calcular:
        - Total de clientes
        - Total de medições
        - Média de peso
        - Clientes com atividade recente
        
        Args:
            nutricionista_id: ID do nutricionista
            
        Returns:
            Dict com métricas e informações dos clientes
            
        Raises:
            ValueError: Se nutricionista não existe
        """
        from models.cliente import Cliente
        from models.medicao import Medicao
        
        # Verificar que nutricionista existe
        nutricionista = self.get_by_id(nutricionista_id)
        if not nutricionista:
            raise ValueError(f"Nutricionista com ID {nutricionista_id} não encontrado")
        
        # Query 1: Total de clientes (count simples)
        total_clientes = self.db.query(func.count(Cliente.id)).filter(
            Cliente.nutricionista_id == nutricionista_id
        ).scalar() or 0
        
        # Query 2: Total de medições (count simples)
        total_medicoes = self.db.query(func.count(Medicao.id)).join(
            Cliente, Medicao.cliente_id == Cliente.id
        ).filter(
            Cliente.nutricionista_id == nutricionista_id
        ).scalar() or 0
        
        # Query 3: Média de peso (avg com tratamento de null)
        # Pega a última medição de cada cliente e calcula a média
        media_peso = self.db.query(func.avg(Medicao.peso)).join(
            Cliente, Medicao.cliente_id == Cliente.id
        ).filter(
            Cliente.nutricionista_id == nutricionista_id,
            Medicao.data_medicao == self.db.query(func.max(Medicao.data_medicao)).join(
                Cliente, Medicao.cliente_id == Cliente.id
            ).filter(
                Cliente.nutricionista_id == nutricionista_id,
                Medicao.cliente_id == Cliente.id
            ).correlate(Cliente).scalar_subquery()
        ).scalar()
        
        # Query 4: Clientes ativos (com medições no último mês)
        data_limite = datetime.utcnow() - timedelta(days=30)
        num_clientes_ativos = self.db.query(func.count(func.distinct(Cliente.id))).join(
            Medicao, Cliente.id == Medicao.cliente_id
        ).filter(
            Cliente.nutricionista_id == nutricionista_id,
            Medicao.data_medicao >= data_limite
        ).scalar() or 0
        
        # Query 5: Últimos 5 clientes com atividade recente (names, latest measurements)
        # Subquery para pegar a última medição de cada cliente
        ultima_medicao_por_cliente = self.db.query(
            Medicao.cliente_id,
            func.max(Medicao.data_medicao).label("data_ultima"),
            func.first_value(Medicao.peso).over(
                partition_by=Medicao.cliente_id,
                order_by=Medicao.data_medicao.desc()
            ).label("peso_ultima")
        ).filter(
            Medicao.cliente_id.in_(
                self.db.query(Cliente.id).filter(
                    Cliente.nutricionista_id == nutricionista_id
                )
            )
        ).distinct().subquery()
        
        clientes_recentes = self.db.query(
            Cliente.id,
            Cliente.nome,
            Cliente.idade,
            Cliente.objetivo,
            ultima_medicao_por_cliente.c.peso_ultima,
            ultima_medicao_por_cliente.c.data_ultima
        ).outerjoin(
            ultima_medicao_por_cliente,
            Cliente.id == ultima_medicao_por_cliente.c.cliente_id
        ).filter(
            Cliente.nutricionista_id == nutricionista_id
        ).order_by(
            ultima_medicao_por_cliente.c.data_ultima.desc().nullslast()
        ).limit(5).all()
        
        # Converter resultados em dicts
        clientes_info = [
            {
                "id": cliente[0],
                "nome": cliente[1],
                "idade": cliente[2],
                "objetivo": cliente[3],
                "ultima_medicao": cliente[4],
                "data_ultima_medicao": cliente[5],
            }
            for cliente in clientes_recentes
        ]
        
        return {
            "nutricionista_id": nutricionista_id,
            "nome": nutricionista.nome,
            "email": nutricionista.email,
            "metricas": {
                "total_clientes": total_clientes,
                "total_medicoes": total_medicoes,
                "media_peso": float(media_peso) if media_peso else None,
                "num_clientes_ativos": num_clientes_ativos,
            },
            "clientes_recentes": clientes_info,
            "configuracao": nutricionista.configuracao,
        }
