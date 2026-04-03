"""Serviço para gerenciamento de Clientes."""
from typing import List, Optional
from sqlalchemy.orm import Session

from models.cliente import Cliente
from schemas.cliente import ClienteCreate, ClienteUpdate
from services.base import BaseService


class ClienteService(BaseService[Cliente, ClienteCreate]):
    """
    Serviço para operações com Cliente.
    
    Operações disponíveis:
    - CRUD básico (herdado de BaseService)
    - Buscar clientes por nutricionista
    - Validações específicas
    """

    def __init__(self, db: Session):
        """Inicializa o serviço com o modelo Cliente."""
        super().__init__(model=Cliente, db=db)

    def get_by_nutricionista(self, nutricionista_id: int, skip: int = 0, limit: int = 10) -> List[Cliente]:
        """
        Busca todos os clientes de um nutricionista.
        
        Args:
            nutricionista_id: ID do nutricionista
            skip: Número de registros a pular (paginação)
            limit: Número máximo de registros a retornar
            
        Returns:
            List[Cliente]: Lista de clientes do nutricionista
        """
        return (
            self.db.query(self.model)
            .filter(self.model.nutricionista_id == nutricionista_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_nutricionista(self, nutricionista_id: int) -> int:
        """
        Conta o total de clientes de um nutricionista.
        
        Args:
            nutricionista_id: ID do nutricionista
            
        Returns:
            int: Total de clientes
        """
        return self.db.query(self.model).filter(
            self.model.nutricionista_id == nutricionista_id
        ).count()

    def create_cliente(self, nutricionista_id: int, cliente_data: ClienteCreate) -> Cliente:
        """
        Cria um novo cliente para um nutricionista.
        
        Args:
            nutricionista_id: ID do nutricionista (proprietário)
            cliente_data: Dados do cliente a criar
            
        Returns:
            Cliente: Cliente criado
            
        Raises:
            ValueError: Se nutricionista_id não corresponder ao schema
        """
        # Verificar se o nutricionista_id fornecido corresponde ao da rota
        if cliente_data.nutricionista_id != nutricionista_id:
            raise ValueError("Cliente deve estar vinculado ao nutricionista correto")
        
        # Usar get_validated_data para normalizar campos en/pt-BR
        validated_data = cliente_data.get_validated_data()
        
        # Converter schema para dicionário e criar cliente
        db_cliente = self.model(**validated_data)
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    def update_cliente(self, cliente_id: int, cliente_data: ClienteUpdate) -> Optional[Cliente]:
        """
        Atualiza um cliente existente.
        
        Args:
            cliente_id: ID do cliente a atualizar
            cliente_data: Dados a atualizar
            
        Returns:
            Optional[Cliente]: Cliente atualizado ou None se não encontrado
        """
        db_cliente = self.get_by_id(cliente_id)
        if not db_cliente:
            return None
        
        # Atualizar apenas campos fornecidos
        update_data = cliente_data.model_dump(exclude_unset=True)
        
        # Normalizar nomes de campos en/pt-BR
        normalized_data = {}
        for field, value in update_data.items():
            if value is not None:  # Ignorar None
                if field == 'name' or field == 'nome':
                    if cliente_data.nome is not None:
                        normalized_data['nome'] = cliente_data.nome
                    elif cliente_data.name is not None:
                        normalized_data['nome'] = cliente_data.name
                elif field == 'age' or field == 'idade':
                    if cliente_data.idade is not None:
                        normalized_data['idade'] = cliente_data.idade
                    elif cliente_data.age is not None:
                        normalized_data['idade'] = cliente_data.age
                elif field == 'height' or field == 'altura':
                    if cliente_data.altura is not None:
                        normalized_data['altura'] = cliente_data.altura
                    elif cliente_data.height is not None:
                        normalized_data['altura'] = cliente_data.height
                elif field == 'objective' or field == 'objetivo':
                    if cliente_data.objetivo is not None:
                        normalized_data['objetivo'] = cliente_data.objetivo
                    elif cliente_data.objective is not None:
                        normalized_data['objetivo'] = cliente_data.objective
        
        for field, value in normalized_data.items():
            setattr(db_cliente, field, value)
        
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    def delete_cliente(self, cliente_id: int) -> bool:
        """
        Deleta um cliente.
        
        Args:
            cliente_id: ID do cliente a deletar
            
        Returns:
            bool: True se deletado com sucesso, False se não encontrado
        """
        db_cliente = self.get_by_id(cliente_id)
        if not db_cliente:
            return False
        
        self.db.delete(db_cliente)
        self.db.commit()
        return True

    def get_cliente_por_nutricionista(self, cliente_id: int, nutricionista_id: int) -> Optional[Cliente]:
        """
        Busca um cliente específico verificando se pertence ao nutricionista.
        
        Útil para autorização: verificar que o cliente pertence ao nutricionista logado.
        
        Args:
            cliente_id: ID do cliente
            nutricionista_id: ID do nutricionista
            
        Returns:
            Optional[Cliente]: Cliente se pertencer ao nutricionista, None caso contrário
        """
        return (
            self.db.query(self.model)
            .filter(
                self.model.id == cliente_id,
                self.model.nutricionista_id == nutricionista_id,
            )
            .first()
        )

    def get_cliente_por_token(self, token: str) -> Optional[Cliente]:
        """
        Busca um cliente através de seu token de acesso público.
        
        Usado para acesso público sem autenticação tradicional.
        
        Args:
            token: Token único do cliente
            
        Returns:
            Optional[Cliente]: Cliente se token válido, None caso contrário
        """
        from models.token_acesso import TokenAcessoCliente
        
        token_obj = (
            self.db.query(TokenAcessoCliente)
            .filter(TokenAcessoCliente.token_unico == token)
            .first()
        )
        
        if not token_obj:
            return None
        
        return token_obj.cliente
