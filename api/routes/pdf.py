"""PDF generation routes."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from core.database import get_db
from services.pdf_service import PDFService
from schemas.base import ErrorResponse

router = APIRouter(prefix="/pdf", tags=["PDF"])


@router.post("/cliente/{cliente_id}/download")
async def download_relatorio_cliente(
    cliente_id: int,
    notas: Optional[str] = None,
    filename: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Generate and download a PDF report for a specific client.
    
    - **cliente_id**: Client ID
    - **notas**: Additional notes to include
    - **filename**: Custom filename for download (default: cliente_{id}_relatorio.pdf)
    """
    try:
        pdf_io = PDFService.gerar_relatorio_cliente(
            db, cliente_id, notas=notas
        )
        
        if not filename:
            filename = f"cliente_{cliente_id}_relatorio.pdf"
        
        return StreamingResponse(
            pdf_io,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@router.get("/cliente/{cliente_id}/inline")
async def visualizar_relatorio_cliente(
    cliente_id: int,
    notas: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Generate and view a PDF report for a specific client inline in browser.
    
    - **cliente_id**: Client ID
    - **notas**: Additional notes to include
    """
    try:
        pdf_io = PDFService.gerar_relatorio_cliente(
            db, cliente_id, notas=notas
        )
        
        return StreamingResponse(
            pdf_io,
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=relatorio.pdf"},
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@router.get("/templates")
async def listar_templates():
    """
    List all available PDF templates.
    
    Returns a list of template filenames that can be used for PDF generation.
    """
    try:
        templates = PDFService.listar_templates()
        return {"templates": templates, "count": len(templates)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list templates: {str(e)}")
