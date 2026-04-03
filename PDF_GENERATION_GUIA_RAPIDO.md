# PDF Generation System - Quick Start Guide

## 30-Second Setup

```bash
# Install system dependencies (macOS)
brew install glib cairo pango gdk-pixbuf libffi

# Install Python packages
pip install WeasyPrint==68.1 Jinja2==3.1.6

# You're done! PDF system is ready to use
```

## 5-Minute Integration

### 1. Generate PDF in Your Code

```python
from services.pdf_service import PDFService
from core.database import SessionLocal

db = SessionLocal()

# Generate PDF
pdf_io = PDFService.gerar_relatorio_cliente(
    db=db,
    cliente_id=1,  # Your client ID
    notas="Follow-up scheduled"
)

# Save or stream it
with open("report.pdf", "wb") as f:
    f.write(pdf_io.getvalue())
```

### 2. Use the Web API

```bash
# Download PDF
curl -X POST "http://localhost:8000/pdf/cliente/1/download" \
  --output report.pdf

# View in browser
open "http://localhost:8000/pdf/cliente/1/inline"

# List templates
curl "http://localhost:8000/pdf/templates"
```

### 3. Use in JavaScript

```javascript
// Download PDF
async function downloadReport(clientId) {
    const response = await fetch(`/pdf/cliente/${clientId}/download`, {
        method: 'POST'
    });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'report.pdf';
    a.click();
}

downloadReport(1);
```

## Common Tasks

### Add Notes to PDF

```python
# Python
pdf_io = PDFService.gerar_relatorio_cliente(
    db, cliente_id=1,
    notas="Client shows improvement in weight management"
)
```

```bash
# cURL
curl -X POST "http://localhost:8000/pdf/cliente/1/download?notas=Client%20improved" \
  --output report.pdf
```

### Customize Colors in Template

Edit `templates/relatorio_cliente.html`:

```html
<style>
    :root {
        --primary-color: #2E7D32;  /* Change this color */
    }
</style>
```

### Add New Content to Template

Edit `templates/relatorio_cliente.html`:

```html
<div class="new-section">
    <h2>Your New Section</h2>
    <p>{{ dados_adicionais.your_field }}</p>
</div>
```

Then pass data:

```python
pdf_io = PDFService.gerar_relatorio_cliente(
    db, cliente_id=1,
    dados_adicionais={
        "your_field": "Your value here"
    }
)
```

### Create New Template

1. Create file: `templates/my_template.html`
2. Use variables: `{{ cliente.nome }}`, `{{ nutricionista.crn }}`, etc.
3. Generate:

```python
context = {
    "cliente": {"nome": "John", ...},
    "nutricionista": {"nome": "Dr. Jane", ...},
    "configuracao": {"cor_primaria": "#2E7D32"},
    "data_geracao": "01/01/2024 as 10:30",
    "dados_adicionais": {},
    "notas": ""
}

pdf_io = PDFService.gerar_pdf_customizado("my_template.html", context)
```

## API Endpoints

### Download PDF

```
POST /pdf/cliente/{cliente_id}/download
?notas=optional_notes
&filename=custom_filename.pdf
```

### View PDF Inline

```
GET /pdf/cliente/{cliente_id}/inline
?notas=optional_notes
```

### List Templates

```
GET /pdf/templates
```

## Template Variables Reference

```python
# Available in all templates:
{{ cliente.nome }}              # Client name
{{ cliente.idade }}             # Client age
{{ cliente.email }}             # Client email
{{ cliente.peso }}              # Client weight
{{ cliente.altura }}            # Client height

{{ nutricionista.nome }}        # Nutritionist name
{{ nutricionista.crn }}         # Nutritionist CRN

{{ configuracao.cor_primaria }} # Primary color e.g. "#2E7D32"
{{ configuracao.logo_url }}     # Logo file path
{{ logo_url }}                  # Full file:// URL to logo

{{ data_geracao }}              # Date/time e.g. "01/01/2024 as 10:30"
{{ notas }}                     # Additional notes

{{ dados_adicionais.key }}      # Custom data
```

## Troubleshooting

### ❌ "cannot load library 'libgobject-2.0-0'"

```bash
brew install glib cairo pango gdk-pixbuf libffi
```

### ❌ "TemplateNotFound: relatorio_cliente.html"

```bash
# Check template exists
ls -la templates/relatorio_cliente.html

# Verify filename spelling
```

### ❌ "Logo not showing in PDF"

```python
# Make sure you have absolute path
logo_path = "/Users/hugo/Desktop/nutri saas/uploads/logo.png"
# NOT relative path: "uploads/logo.png"
```

### ❌ "PDF generation is slow"

1. Make logo file smaller (<500KB)
2. Simplify CSS in template
3. Optimize database queries

## Files Overview

```
templates/relatorio_cliente.html  - Main PDF template
services/pdf_service.py          - PDF generation logic
api/routes/pdf.py                - API endpoints
test_pdf_generation.py           - Tests
PDF_GENERATION_DOCUMENTATION.md  - Full documentation
```

## Running Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run tests
pytest test_pdf_generation.py -v

# With coverage
pytest test_pdf_generation.py --cov
```

## Example: Complete Workflow

```python
from services.pdf_service import PDFService
from core.database import SessionLocal
from models.cliente import Cliente

# 1. Get database session
db = SessionLocal()

# 2. Find client
client = db.query(Cliente).filter(Cliente.id == 1).first()
if not client:
    print("Client not found")
    exit()

# 3. Generate PDF
try:
    pdf_io = PDFService.gerar_relatorio_cliente(
        db=db,
        cliente_id=client.id,
        notas=f"Follow-up with {client.nutricionista.nome}",
        dados_adicionais={
            "peso_anterior": 75.5,
            "peso_atual": 72.0,
            "progresso": "Excelente"
        }
    )
    
    # 4. Save PDF
    filename = f"relatorio_{client.nome.replace(' ', '_')}_{client.id}.pdf"
    with open(f"downloads/{filename}", "wb") as f:
        f.write(pdf_io.getvalue())
    
    print(f"✅ PDF saved: {filename}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")

finally:
    db.close()
```

## Next Steps

- 📖 Read [PDF_GENERATION_DOCUMENTATION.md](PDF_GENERATION_DOCUMENTATION.md) for complete reference
- 🧪 Run tests: `pytest test_pdf_generation.py -v`
- 🎨 Customize `templates/relatorio_cliente.html` for your branding
- 🚀 Deploy to production

## Need Help?

1. Check [PDF_GENERATION_DOCUMENTATION.md](PDF_GENERATION_DOCUMENTATION.md)
2. Run tests to verify setup: `pytest test_pdf_generation.py`
3. Check project ARCHITECTURE.md for system overview
