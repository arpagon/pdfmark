# PDFMark

A tool to add beautiful gradient watermarks to PDF files using wave patterns and rainbow colors.

## 🌐 Live Preview Tool

**Try the interactive watermark preview tool:** https://arpagon.github.io/pdfmark/watermark_preview.html

Load images, adjust parameters in real-time, and export watermarked images directly from your browser!

## ⚠️ Current Status

**Note**: The Python CLI watermarking process is currently under development and may not work correctly. Use the web preview tool for reliable watermark generation.

## Features

- Add gradient wave pattern watermarks to PDF files
- Rainbow color scheme inspired by modern design patterns
- Simple command-line interface
- Preserves original PDF quality

## Installation

Make sure you have `uv` installed, then:

```bash
git clone https://github.com/arpagon/pdfmark.git
cd pdfmark
uv sync
```

## Usage

```bash
uv run pdfmark input.pdf output.pdf
```

## Requirements

- Python 3.8+
- uv package manager

## Dependencies

The tool uses modern Python libraries for PDF manipulation and graphics generation to create wave-pattern watermarks with gradient colors.