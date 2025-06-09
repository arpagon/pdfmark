# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PDFMark is a Python tool that adds gradient wave pattern watermarks to PDF files using rainbow colors. The project uses modern Python libraries for PDF manipulation and graphics generation.

## Development Commands

- **Install dependencies**: `uv sync`
- **Run the tool**: `uv run python main.py input.pdf output.pdf`
- **Create sample PDF**: `uv run python sample.py`
- **Install as package**: `uv pip install -e .` (then use `uv run pdfmark`)

## CLI Options

- `--opacity, -o`: Watermark opacity (0.1-1.0, default: 0.3)
- `--waves, -w`: Number of wave cycles (default: 3)

## Project Structure

- `main.py`: Typer CLI interface with argument validation
- `watermark.py`: Core watermarking functionality with rainbow gradients and wave patterns
- `sample.py`: Utility to create test PDF files
- Uses `uv` package manager with modern Python dependencies

## Key Architecture

- **Rainbow Gradient Generation**: HSV color space conversion for smooth rainbow transitions
- **Wave Pattern Creation**: Mathematical sine wave generation with polygon filling
- **PDF Processing**: PyPDF2 for reading/writing, ReportLab for watermark overlay
- **Image Processing**: PIL for gradient creation and alpha blending