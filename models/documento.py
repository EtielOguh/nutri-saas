"""Modelo de Documento PDF."""
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel

if TYPE_CHECKING:
    from models.cliente import Cliente  # noqa: F401


class DocumentoPDF(BaseModel):
    """
    Modelo de Documento PDF.
    
    Armazena referências a documentos PDF relacionados ao cliente.
    Pode ser relatórios, guias nutricionais, etc.
    """

    __tablename__ = "documentos_pdf"

    # Foreign Key
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Campos
    url_pdf: Mapped[str] = mapped_column(String(512), nullable=False)

    # Relacionamento (usar strings para evitar circular imports)
    cliente: Mapped["Cliente"] = relationship(
        "Cliente",
        back_populates="documentos",
        lazy="selectin",
    )

    # Índices
    __table_args__ = (
        Index("idx_documento_cliente_id", "cliente_id"),
    )

    def __repr__(self) -> str:
        return f"<DocumentoPDF(id={self.id}, cliente_id={self.cliente_id})>"
