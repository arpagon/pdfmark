import typer
from pathlib import Path
from watermark import create_watermark_image

app = typer.Typer(help="Preview watermark patterns before applying to PDF")

@app.command()
def preview(
    width: int = typer.Option(800, "--width", "-w", help="Image width in pixels"),
    height: int = typer.Option(600, "--height", "-h", help="Image height in pixels"),
    opacity: float = typer.Option(0.3, "--opacity", "-o", help="Watermark opacity (0.1-1.0)"),
    wave_frequency: int = typer.Option(3, "--waves", help="Number of wave cycles"),
    text: str = typer.Option("WATERMARK", "--text", "-t", help="Text to display in wave pattern"),
    output: str = typer.Option("watermark_preview.png", "--output", help="Output PNG filename"),
):
    """Generate a PNG preview of the watermark pattern."""
    
    if opacity < 0.01 or opacity > 1.0:
        typer.echo(f"Error: Opacity must be between 0.01 and 1.0", err=True)
        raise typer.Exit(1)
    
    try:
        # Create watermark image
        watermark_img = create_watermark_image(width, height, wave_frequency, opacity, text)
        
        # Save as PNG
        watermark_img.save(output, format='PNG')
        typer.echo(f"✓ Watermark preview saved: {output}")
        typer.echo(f"  Size: {width}x{height}")
        typer.echo(f"  Opacity: {opacity}")
        typer.echo(f"  Wave frequency: {wave_frequency}")
        
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()