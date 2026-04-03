"""Modelo de Cliente."""
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Float, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel

if TYPE_CHECKING:
    from models.nutricionista import Nutricionista  # noqa: F401
    from models.medicao import Medicao  # noqa: F401
    from models.observacao import Observacao  # noqa: F401
    from models.token_acesso import TokenAcessoCliente  # noqa: F401
    from models.documento import DocumentoPDF  # noqa: F401


class Cliente(BaseModel):
    """
    Modelo de Cliente (Paciente).
    
    Representa um cliente/paciente de um nutricionista.
    """

    __tablename__ = "clientes"

    # Foreign Key
    nutricionista_id: Mapped[int] = mapped_column(
        ForeignKey("nutricionistas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Campos
    nome: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    idade: Mapped[int | None] = mapped_column(Integer, nullable=True)
    altura: Mapped[float | None] = mapped_column(Float, nullable=True)  # Em centímetros
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    initial_weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    objetivo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)

    # Relacionamentos (usar strings para evitar circular imports)
    nutricionista: Mapped["Nutricionista"] = relationship(
        "Nutricionista",
        back_populates="clientes",
        lazy="selectin",
    )
    medicoes: Mapped[List["Medicao"]] = relationship(
        "Medicao",
        back_populates="cliente",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    observacoes: Mapped[List["Observacao"]] = relationship(
        "Observacao",
        back_populates="cliente",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    token_acesso: Mapped[Optional["TokenAcessoCliente"]] = relationship(
        "TokenAcessoCliente",
        back_populates="cliente",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    documentos: Mapped[List["DocumentoPDF"]] = relationship(
        "DocumentoPDF",
        back_populates="cliente",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # Índices
    __table_args__ = (
        Index("idx_cliente_nutricionista_id", "nutricionista_id"),
        Index("idx_cliente_nome", "nome"),
    )

    def __repr__(self) -> str:
        return f"<Cliente(id={self.id}, nome='{self.nome}', nutricionista_id={self.nutricionista_id})>"
