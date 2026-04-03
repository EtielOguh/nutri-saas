"""Modelo de Nutricionista."""
from typing import TYPE_CHECKING, List
from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel

if TYPE_CHECKING:
    from models.cliente import Cliente  # noqa: F401


class Nutricionista(BaseModel):
    """
    Modelo de Nutricionista.
    
    Representa um profissional nutricionista no sistema.
    """

    __tablename__ = "nutricionistas"

    # Campos
    nome: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relacionamentos (usar strings para evitar circular imports)
    clientes: Mapped[List["Cliente"]] = relationship(
        "Cliente",
        back_populates="nutricionista",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    configuracao: Mapped["ConfiguracaoNutricionista"] = relationship(
        "ConfiguracaoNutricionista",
        back_populates="nutricionista",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # Índices
    __table_args__ = (
        Index("idx_nutricionista_email", "email"),
    )

    def __repr__(self) -> str:
        return f"<Nutricionista(id={self.id}, nome='{self.nome}', email='{self.email}')>"


class ConfiguracaoNutricionista(BaseModel):
    """
    Configurações personalizadas do nutricionista.
    
    Armazena informações como logo, cor primária, valor de consulta, etc.
    """

    __tablename__ = "configuracoes_nutricionista"

    # Foreign Key
    nutricionista_id: Mapped[int] = mapped_column(
        ForeignKey("nutricionistas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        primary_key=True,
    )

    # Campos
    logo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    cor_primaria: Mapped[str] = mapped_column(String(7), default="#0066CC")  # Formato hex
    valor_consulta: Mapped[float] = mapped_column(nullable=False, default=0.0)
    link_agendamento: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # Relacionamento
    nutricionista: Mapped["Nutricionista"] = relationship(
        "Nutricionista",
        back_populates="configuracao",
        lazy="selectin",
    )

    # Índices
    __table_args__ = (
        Index("idx_config_nutricionista_id", "nutricionista_id"),
    )

    def __repr__(self) -> str:
        return f"<ConfiguracaoNutricionista(nutricionista_id={self.nutricionista_id})>"
