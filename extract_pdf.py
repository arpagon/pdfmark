import fitz  # PyMuPDF
import typer
from pathlib import Path

def extract_pdf_as_image(pdf_path: str, output_path: str = "pdf_page.png", page_num: int = 0):
    """Extract a PDF page as an image."""
    
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    if page_num >= len(doc):
        typer.echo(f"Error: Page {page_num} doesn't exist. PDF has {len(doc)} pages.")
        return
    
    # Get the specified page
    page = doc[page_num]
    
    # Render page to an image (higher DPI for better quality)
    mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
    pix = page.get_pixmap(matrix=mat)
    
    # Save as PNG
    pix.save(output_path)
    
    doc.close()
    
    typer.echo(f"✓ PDF page extracted as: {output_path}")
    typer.echo(f"  Page: {page_num}")
    typer.echo(f"  Size: {pix.width}x{pix.height}")

if __name__ == "__main__":
    typer.run(extract_pdf_as_image)