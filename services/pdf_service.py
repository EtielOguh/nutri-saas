"""PDF generation service using WeasyPrint and Jinja2."""
from pathlib import Path
from datetime import datetime
from io import BytesIO
from typing import Optional, Dict, Any

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from sqlalchemy.orm import Session

from models.cliente import Cliente
from models.nutricionista import Nutricionista


TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


class PDFService:
    """Service for PDF generation with WeasyPrint and Jinja2."""

    @staticmethod
    def gerar_relatorio_cliente(
        db,
        cliente_id,
        dados_adicionais=None,
        notas=None,
        logo_path=None,
    ):
        """Generates a PDF report of the client."""
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            raise ValueError(f"Cliente {cliente_id} not found")
        
        nutricionista = db.query(Nutricionista).filter(
            Nutricionista.id == cliente.nutricionista_id
        ).first()
        if not nutricionista:
            raise ValueError("Nutricionista not found")
        
        config = nutricionista.configuracao
        if not config:
            raise ValueError("Configuracao not found")
        
        if logo_path is None and config.logo_url:
            logo_path = config.logo_url.lstrip("/")
        
        logo_url = None
        if logo_path:
            lp = Path(logo_path)
            if lp.exists():
                logo_url = f"file://{lp.absolute()}"
        
        ctx = {
            "cliente": cliente,
            "nutricionista": nutricionista,
            "configuracao": config,
            "logo_url": logo_url,
            "data_geracao": datetime.now().strftime("%d/%m/%Y as %H:%M"),
            "dados_adicionais": dados_adicionais or {},
            "notas": notas,
        }
        
        template = jinja_env.get_template("relatorio_cliente.html")
        html = template.render(**ctx)
        pdf_bytes = HTML(string=html).write_pdf()
        f = BytesIO(pdf_bytes)
        f.seek(0)
        return f
    
    @staticmethod
    def gerar_pdf_customizado(template_name, context):
        """Generates a PDF from a custom template."""
        template = jinja_env.get_template(template_name)
        html = template.render(**context)
        pdf_bytes = HTML(string=html).write_pdf()
        f = BytesIO(pdf_bytes)
        f.seek(0)
        return f
    
    @staticmethod
    def listar_templates():
        """Lists all available templates."""
        if not TEMPLATES_DIR.exists():
            return []
        return sorted(
            n for n in [str(f.name) for f in TEMPLATES_DIR.glob("*.html")]
            if not n.startswith("_")
        )
