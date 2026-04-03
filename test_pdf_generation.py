"""Tests for PDF generation system."""
import pytest
from datetime import datetime
from io import BytesIO
from unittest.mock import Mock, MagicMock, patch

from services.pdf_service import PDFService


class TestPDFService:
    """Test cases for PDFService."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        return Mock()

    @pytest.fixture
    def mock_cliente(self):
        """Create a mock Cliente object."""
        cliente = Mock()
        cliente.id = 1
        cliente.nome = "João Silva"
        cliente.idade = 30
        cliente.email = "joao@example.com"
        cliente.nutricionista_id = 1
        return cliente

    @pytest.fixture
    def mock_nutricionista(self):
        """Create a mock Nutricionista object."""
        nutricionista = Mock()
        nutricionista.id = 1
        nutricionista.nome = "Dra. Maria"
        nutricionista.crn = "12345"
        return nutricionista

    @pytest.fixture
    def mock_configuracao(self):
        """Create a mock ConfiguracaoNutricionista object."""
        config = Mock()
        config.cor_primaria = "#2E7D32"
        config.logo_url = None
        config.descricao_rodape = "Consultório Nutricional"
        return config

    def test_gerar_relatorio_cliente_success(self, mock_db, mock_cliente, mock_nutricionista, mock_configuracao):
        """Test successful PDF generation for a client."""
        mock_nutricionista.configuracao = mock_configuracao
        
        mock_db.query.return_value.filter.return_value.first.side_effect = [
            mock_cliente,
            mock_nutricionista,
        ]
        
        result = PDFService.gerar_relatorio_cliente(mock_db, cliente_id=1)
        
        assert isinstance(result, BytesIO)
        assert result.tell() == 0  # Position should be at beginning after seek(0)
        pdf_content = result.read()
        assert len(pdf_content) > 0  # PDF should have content
        assert pdf_content.startswith(b"%PDF")  # Valid PDF header

    def test_gerar_relatorio_cliente_not_found(self, mock_db):
        """Test PDF generation when cliente is not found."""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with pytest.raises(ValueError, match="Cliente 999 not found"):
            PDFService.gerar_relatorio_cliente(mock_db, cliente_id=999)

    def test_gerar_relatorio_cliente_with_notas(self, mock_db, mock_cliente, mock_nutricionista, mock_configuracao):
        """Test PDF generation with additional notes."""
        mock_nutricionista.configuracao = mock_configuracao
        
        mock_db.query.return_value.filter.return_value.first.side_effect = [
            mock_cliente,
            mock_nutricionista,
        ]
        
        notas = "Cliente apresenta deficiência de Vitamina D"
        result = PDFService.gerar_relatorio_cliente(
            mock_db, cliente_id=1, notas=notas
        )
        
        assert isinstance(result, BytesIO)
        pdf_content = result.read()
        assert pdf_content.startswith(b"%PDF")

    def test_listar_templates(self):
        """Test listing available templates."""
        templates = PDFService.listar_templates()
        
        assert isinstance(templates, list)
        # Should contain our main template
        assert "relatorio_cliente.html" in templates

    def test_listar_templates_no_directory(self):
        """Test listing templates when directory doesn't exist."""
        with patch('services.pdf_service.TEMPLATES_DIR') as mock_dir:
            mock_dir.exists.return_value = False
            
            templates = PDFService.listar_templates()
            
            assert templates == []

    def test_gerar_pdf_customizado(self, mock_db):
        """Test generating PDF from custom template."""
        template_name = "relatorio_cliente.html"
        context = {
            "cliente": {"nome": "Test Client", "idade": 25},
            "nutricionista": {"nome": "Test Nutritionist"},
            "configuracao": {"cor_primaria": "#2E7D32"},
            "data_geracao": datetime.now().strftime("%d/%m/%Y as %H:%M"),
        }
        
        result = PDFService.gerar_pdf_customizado(template_name, context)
        
        assert isinstance(result, BytesIO)
        pdf_content = result.read()
        assert pdf_content.startswith(b"%PDF")

    def test_pdf_output_is_readable(self, mock_db, mock_cliente, mock_nutricionista, mock_configuracao):
        """Test that generated PDF can be read multiple times."""
        mock_nutricionista.configuracao = mock_configuracao
        
        mock_db.query.return_value.filter.return_value.first.side_effect = [
            mock_cliente,
            mock_nutricionista,
        ]
        
        result = PDFService.gerar_relatorio_cliente(mock_db, cliente_id=1)
        
        # Read PDF content
        pdf_content_1 = result.read()
        assert len(pdf_content_1) > 0
        
        # Seek to beginning and read again
        result.seek(0)
        pdf_content_2 = result.read()
        
        # Contents should be identical
        assert pdf_content_1 == pdf_content_2


class TestPDFIntegration:
    """Integration tests for PDF system endpoints."""

    @pytest.fixture
    def test_client(self):
        """Create a test FastAPI client."""
        from fastapi.testclient import TestClient
        from main import app
        
        return TestClient(app)

    def test_pdf_templates_endpoint(self, test_client):
        """Test /pdf/templates endpoint."""
        response = test_client.get("/pdf/templates")
        
        assert response.status_code == 200
        data = response.json()
        assert "templates" in data
        assert "count" in data
        assert isinstance(data["templates"], list)

    def test_pdf_download_endpoint_not_found(self, test_client):
        """Test /pdf/cliente/{id}/download with non-existent client."""
        response = test_client.post("/pdf/cliente/99999/download")
        
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
