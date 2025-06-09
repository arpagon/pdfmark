from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample_pdf(filename: str = "sample.pdf"):
    """Create a simple sample PDF for testing."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Add title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Sample PDF Document")
    
    # Add some content
    c.setFont("Helvetica", 12)
    y = height - 150
    lines = [
        "This is a sample PDF document created for testing the pdfmark tool.",
        "",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco.",
        "",
        "The rainbow wave watermark should appear over this content.",
        "You should be able to see beautiful gradient colors flowing",
        "in wave patterns across the page while preserving readability.",
    ]
    
    for line in lines:
        c.drawString(100, y, line)
        y -= 20
    
    c.save()
    print(f"Created sample PDF: {filename}")

if __name__ == "__main__":
    create_sample_pdf()