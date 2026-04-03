"""Modelo de Medição."""
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel

if TYPE_CHECKING:
    from models.cliente import Cliente  # noqa: F401


class Medicao(BaseModel):
    """
    Modelo de Medição.
    
    Armazena registros de peso e data de medição de cada cliente.
    """

    __tablename__ = "medicoes"

    # Foreign Key
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Campos
    peso: Mapped[float] = mapped_column(Float, nullable=False)  # Em kg
    data_medicao: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    # Relacionamento (usar strings para evitar circular imports)
    cliente: Mapped["Cliente"] = relationship(
        "Cliente",
        back_populates="medicoes",
        lazy="selectin",
    )

    # Índices
    __table_args__ = (
        Index("idx_medicao_cliente_id", "cliente_id"),
        Index("idx_medicao_data", "data_medicao"),
        Index("idx_medicao_cliente_data", "cliente_id", "data_medicao"),
    )

    def __repr__(self) -> str:
        return f"<Medicao(id={self.id}, cliente_id={self.cliente_id}, peso={self.peso}kg)>"
