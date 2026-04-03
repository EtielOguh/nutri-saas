# PDF Generation System Documentation

## Overview

The PDF Generation System provides functionality to generate professional PDF reports for clients using WeasyPrint and Jinja2 templating. This system integrates with the existing FastAPI application to create downloadable or viewable PDF documents with client data, nutritionist information, and customizable styling.

## Architecture

### Components

1. **PDFService** (`services/pdf_service.py`)
   - Core service for PDF generation
   - Handles template rendering and PDF conversion
   - Manages template discovery

2. **PDF Routes** (`api/routes/pdf.py`)
   - REST API endpoints for PDF operations
   - Handles requests for PDF download and viewing
   - Returns streamed PDF responses

3. **HTML Templates** (`templates/`)
   - Jinja2 templates for PDF content
   - Main template: `relatorio_cliente.html`
   - Supports dynamic variable injection

4. **Tests** (`test_pdf_generation.py`)
   - Unit tests for PDFService
   - Integration tests for endpoints
   - Mock-based testing

## Installation & Setup

### System Dependencies

WeasyPrint requires system libraries for text rendering on macOS:

```bash
brew install glib cairo pango gdk-pixbuf libffi
```

### Python Dependencies

All required packages are installed via `requirements.txt`:

```bash
pip install WeasyPrint==68.1 Jinja2==3.1.6
```

Includes:
- **WeasyPrint**: PDF generation from HTML/CSS
- **Jinja2**: Template rendering engine
- **MarkupSafe**, **Pillow**, **Pyphen**, **brotli**: Supporting libraries

## API Endpoints

### 1. Download Client Report PDF

**POST** `/pdf/cliente/{cliente_id}/download`

Download a PDF report for a specific client.

**Parameters:**
- `cliente_id` (int, path): Client ID
- `notas` (str, optional, query): Additional notes to include in PDF
- `filename` (str, optional, query): Custom filename for download

**Response:**
- **200**: PDF file stream (application/pdf)
- **404**: Cliente not found
- **500**: PDF generation failed

**Example:**
```bash
curl -X POST "http://localhost:8000/pdf/cliente/1/download?notas=Follow%20up%20needed" \
  -o client_report.pdf
```

### 2. View Client Report PDF Inline

**GET** `/pdf/cliente/{cliente_id}/inline`

View a PDF report in the browser without downloading.

**Parameters:**
- `cliente_id` (int, path): Client ID
- `notas` (str, optional, query): Additional notes to include

**Response:**
- **200**: PDF file stream (displayed inline)
- **404**: Cliente not found
- **500**: PDF generation failed

**Example:**
```bash
curl "http://localhost:8000/pdf/cliente/1/inline" -o report.pdf
```

### 3. List Available Templates

**GET** `/pdf/templates`

List all available PDF templates.

**Response:**
```json
{
  "templates": ["relatorio_cliente.html"],
  "count": 1
}
```

**Example:**
```bash
curl "http://localhost:8000/pdf/templates"
```

## Template System

### Template Location

All templates are stored in the `templates/` directory at the project root:

```
templates/
├── relatorio_cliente.html    # Main client report template
└── (additional templates...)
```

### Template Variables

The `relatorio_cliente.html` template receives the following context:

```python
{
    "cliente": Cliente,              # Client object with all attributes
    "nutricionista": Nutricionista,  # Nutritionist object
    "configuracao": ConfiguracaoNutricionista,  # Configuration with styling
    "logo_url": str,                # Full file URL to logo
    "data_geracao": str,            # Generation timestamp (DD/MM/YYYY as HH:MM)
    "dados_adicionais": dict,       # Additional key-value data
    "notas": str,                   # Additional notes
}
```

### Template Customization

##### Modify Styling (Colors, Fonts)

Edit `templates/relatorio_cliente.html` CSS section:

```html
<style>
    :root {
        --primary-color: {{ configuracao.cor_primaria }};
        --text-color: #333;
        --background-color: #f9f9f9;
    }
</style>
```

##### Add New Sections

Extend the template with new sections:

```html
<div class="custom-section">
    <h2>Custom Data</h2>
    <p>{{ dados_adicionais.custom_field }}</p>
</div>
```

##### Create New Templates

1. Create new file in `templates/` (e.g., `relatorio_nitrientes.html`)
2. Use same variable names as `relatorio_cliente.html`
3. Use PDFService to generate:

```python
PDFService.gerar_pdf_customizado("relatorio_nitrientes.html", context)
```

## Usage Examples

### Python Code

#### Generate and Save PDF

```python
from services.pdf_service import PDFService
from core.database import SessionLocal

db = SessionLocal()

# Generate PDF
pdf_io = PDFService.gerar_relatorio_cliente(
    db=db,
    cliente_id=1,
    notas="Follow-up required"
)

# Save to file
with open("client_report.pdf", "wb") as f:
    f.write(pdf_io.getvalue())
```

#### Use in FastAPI Endpoint

```python
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from services.pdf_service import PDFService
from core.dependencies import get_db

router = APIRouter()

@router.get("/client/{id}/report")
def get_client_report(id: int, db = Depends(get_db)):
    pdf_io = PDFService.gerar_relatorio_cliente(db, id)
    return StreamingResponse(
        pdf_io,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=report.pdf"}
    )
```

#### List Templates

```python
from services.pdf_service import PDFService

templates = PDFService.listar_templates()
print(templates)  # ['relatorio_cliente.html']
```

### cURL

#### Download PDF

```bash
curl -X POST "http://localhost:8000/pdf/cliente/1/download" \
  --output report.pdf
```

#### Download with Custom Notes

```bash
curl -X POST "http://localhost:8000/pdf/cliente/1/download?notas=Client%20ready%20for%20next%20phase" \
  --output report_with_notes.pdf
```

#### View PDF Inline

```bash
# Opens in browser
curl "http://localhost:8000/pdf/cliente/1/inline"
```

### JavaScript/Fetch

#### Download PDF

```javascript
async function downloadClientReport(clientId) {
    const response = await fetch(`/pdf/cliente/${clientId}/download`, {
        method: 'POST'
    });
    
    if (!response.ok) throw new Error('PDF generation failed');
    
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `client_${clientId}.pdf`;
    link.click();
}
```

#### View PDF in IFrame

```javascript
async function viewClientReport(clientId) {
    const url = `/pdf/cliente/${clientId}/inline`;
    document.getElementById('pdf-viewer').src = url;
}
```

## Database Models

### Cliente
```python
class Cliente(Base):
    id: int
    nome: str
    email: str
    idade: int
    nutricionista_id: int  # Foreign key
    # ... other fields
```

### Nutricionista
```python
class Nutricionista(Base):
    id: int
    nome: str
    crn: str
    # ... other fields
    configuracao: ConfiguracaoNutricionista  # Relationship
```

### ConfiguracaoNutricionista
```python
class ConfiguracaoNutricionista(Base):
    id: int
    nutricionista_id: int
    cor_primaria: str  # e.g., "#2E7D32"
    logo_url: str      # Path to logo file
    descricao_rodape: str
    # ... other fields
```

## File Structure

```
/Users/hugo/Desktop/nutri saas/
├── services/
│   ├── pdf_service.py           # PDF generation service
│   ├── cliente_service.py
│   └── ...
├── api/
│   └── routes/
│       ├── pdf.py               # PDF endpoints
│       └── ...
├── templates/
│   ├── relatorio_cliente.html   # Main template
│   └── (additional templates)
├── uploads/                      # Generated logos stored here
├── test_pdf_generation.py        # Tests
├── main.py                       # Application entry point
└── requirements.txt
```

## Troubleshooting

### Issue: WeasyPrint Library Not Found

**Error:** `OSError: cannot load library 'libgobject-2.0-0'`

**Solution:**
```bash
brew install glib cairo pango gdk-pixbuf libffi
```

Then restart Python environment.

### Issue: Template Not Found

**Error:** `jinja2.exceptions.TemplateNotFound: template_name.html`

**Solution:**
1. Verify template exists in `templates/` directory
2. Check template filename spelling
3. Ensure `templates/` is in project root

### Issue: Logo Not Displaying in PDF

**Problem:** Logo appears blank in generated PDF

**Solution:**
1. Verify logo file exists at `logo_url` path
2. Use absolute file path: `file:///path/to/logo.png`
3. Ensure file is JPEG or PNG format
4. Check image dimensions (not too large)

### Issue: Slow PDF Generation

**Problem:** PDF takes >5 seconds to generate

**Causes:**
- Large images in logo
- Complex CSS styling
- Database queries blocking

**Solutions:**
1. Optimize logo size (<500KB)
2. Simplify CSS in template
3. Pre-load client data
4. Use async endpoints

## Performance Optimization

### Template Caching

Templates are cached by Jinja2 automatically. To clear cache:

```python
from services.pdf_service import jinja_env
jinja_env.cache.clear()
```

### Image Optimization

Keep logo images small:
- **Format:** PNG or JPEG
- **Size:** <500KB
- **Dimensions:** 200x200px recommended

### Database Query Optimization

Use eager loading for relationships:

```python
from sqlalchemy.orm import joinedload

cliente = db.query(Cliente).options(
    joinedload(Cliente.nutricionista),
    joinedload(Cliente.medicoes)
).filter(Cliente.id == client_id).first()
```

## Security Considerations

1. **Access Control**: Verify user owns the client data before generating PDF
2. **File Paths**: Always validate and sanitize custom filename parameter
3. **Template Injection**: Use Jinja2 with autoescape for user content
4. **Rate Limiting**: Implement rate limiting on PDF endpoints
5. **Sensitive Data**: Be cautious including personal health information

## Testing

### Run Tests

```bash
pytest test_pdf_generation.py -v
```

### Run Specific Test

```bash
pytest test_pdf_generation.py::TestPDFService::test_gerar_relatorio_cliente_success -v
```

### Test Coverage

```bash
pytest test_pdf_generation.py --cov=services.pdf_service
```

## Future Enhancements

1. **Multi-format Support**: Add Word, Excel export
2. **Digital Signatures**: Sign PDFs with nutritionist credentials
3. **Batch Generation**: Generate multiple PDFs at once
4. **Email Integration**: Send PDF via email automatically
5. **Template Management**: Admin UI for template creation
6. **Schedule Reports**: Generate periodic reports automatically
7. **Compression**: Compress PDFs to reduce file size
8. **Watermarks**: Add watermarks to PDFs

## Related Documentation

- [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/stable/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [FastAPI Responses](https://fastapi.tiangolo.com/advanced/response-directly/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)

## API Reference

### PDFService Class

#### `gerar_relatorio_cliente(db, cliente_id, dados_adicionais=None, notas=None, logo_path=None)`

Generate a PDF report for a client.

**Parameters:**
- `db` (Session): SQLAlchemy database session
- `cliente_id` (int): ID of the client
- `dados_adicionais` (dict, optional): Additional context data
- `notas` (str, optional): Additional notes to include
- `logo_path` (str, optional): Path to logo file

**Returns:** `BytesIO` object containing PDF data

**Raises:** `ValueError` if client or nutritionist not found

#### `gerar_pdf_customizado(template_name, context)`

Generate a PDF from a custom template.

**Parameters:**
- `template_name` (str): Name of template file in `templates/` directory
- `context` (dict): Template context variables

**Returns:** `BytesIO` object containing PDF data

**Raises:** `jinja2.TemplateNotFound` if template not found

#### `listar_templates()`

List all available PDF templates.

**Returns:** List of template filenames

## Contact & Support

For issues or questions about the PDF Generation System, contact the development team or check the main project documentation.
