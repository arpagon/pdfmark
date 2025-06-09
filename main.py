import typer
from pathlib import Path
from watermark import add_watermark

app = typer.Typer(help="Add beautiful gradient watermarks to PDF files using wave patterns and rainbow colors.")

@app.command()
def main(
    input_pdf: Path = typer.Argument(..., help="Input PDF file path"),
    output_pdf: Path = typer.Argument(..., help="Output PDF file path"),
    opacity: float = typer.Option(0.3, "--opacity", "-o", help="Watermark opacity (0.1-1.0)"),
    wave_frequency: int = typer.Option(3, "--waves", "-w", help="Number of wave cycles"),
    text: str = typer.Option("WATERMARK", "--text", "-t", help="Text to display in wave pattern"),
):
    """Add gradient wave watermark to PDF file."""
    
    if not input_pdf.exists():
        typer.echo(f"Error: Input file '{input_pdf}' does not exist", err=True)
        raise typer.Exit(1)
    
    if not input_pdf.suffix.lower() == '.pdf':
        typer.echo(f"Error: Input file must be a PDF", err=True)
        raise typer.Exit(1)
    
    if opacity < 0.01 or opacity > 1.0:
        typer.echo(f"Error: Opacity must be between 0.01 and 1.0", err=True)
        raise typer.Exit(1)
    
    try:
        add_watermark(input_pdf, output_pdf, opacity, wave_frequency, text)
        typer.echo(f"✓ Watermark added successfully: {output_pdf}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
