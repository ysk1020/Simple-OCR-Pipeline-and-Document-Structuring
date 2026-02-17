
# Simple OCR Pipeline and Document Structuring

A compact OCR processing and document-structuring toolkit designed for research and small-scale experiments with invoice/receipt-style documents. The project demonstrates a minimal end-to-end pipeline: image preprocessing, OCR text + bounding-box extraction, lightweight layout-aware structuring (key/value extraction), result export, and visual debugging.

## Overview

This repository provides a reproducible, easy-to-extend baseline for extracting structured information from scanned documents. It is modular so you can swap OCR engines, improve preprocessing, or experiment with structuring heuristics.

Key capabilities:
- Preprocess images for more reliable OCR (binarization, simple denoising).
- Run OCR using a pluggable engine (Tesseract implemented by default).
- Group tokens and extract key/value pairs using simple layout and lexical rules.
- Export structured outputs as CSV and JSON and generate annotated images for inspection.

## Methods and Components

- `src/preprocess/` — image helpers (binarize, thresholding) to improve OCR quality on noisy scans.
- `src/ocr/` — OCR abstraction plus a `tesseract_engine.py` implementation that returns text with bounding boxes where available.
- `src/structure/` — heuristics for grouping nearby tokens into fields and extracting likely keys and values. Current logic is rule-based and tuned for receipt-like layouts.
- `src/export/` — exporters for CSV and JSON (`to_csv.py`, `to_json.py`). Each processed document produces a JSON representation and optional CSV rows for tabular consumption.
- `src/visualize/` — drawing utilities to annotate images with bounding boxes and labels for debugging.

The pipeline in `run.py` wires these components in sequence: preprocess → OCR → structure → export → visualize.

## Pipeline flow:
```scss
Input image(s)
      ↓
OCR (Tesseract)
      ↓
Token extraction
      ↓
Export (JSON, CSV)
      ↓
Annotated visualization
```
## Setup

Prerequisites
- Python 3.8+ recommended.
- System Tesseract OCR if you want to use the default engine (install with your package manager).

Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Install Tesseract (Ubuntu example)

```bash
sudo apt update
sudo apt install tesseract-ocr libtesseract-dev
```

## Running the pipeline

Basic run

```bash
python run.py
```

The top-level script will read configuration from `src/config.py`. Typical adjustments you may make:
- input/output directories
- enabling/disabling visualization
- selecting OCR engine

Testing OCR integration

```bash
python test_ocr.py
```

This script runs a small, local check of the OCR engine and will produce sample outputs in `results/` and annotated images in `output/annotated_images/`.

Advanced usage
- To process a specific image or folder, modify `run.py` or add a small wrapper that calls the pipeline with your path.
- To add another OCR engine, implement the interface defined in `src/ocr/base.py` and register it in `run.py`.

## Known issues and limitations

- The structuring logic is heuristic and may fail on complex or unusual layouts. Consider integrating learning-based layout models (LayoutLM, TrOCR) for production workloads.
- OCR accuracy depends on image quality and language/charset configuration. Tesseract may require language packs or custom configuration for non-English documents.
- No guarantees on privacy/compliance — avoid pushing sensitive data (PII) to public repositories.

## Implementation status / TODOs

- `src/preprocess/binarize.py`: TODO — binarization code is not implemented yet; currently a placeholder. If you rely on preprocessing, implement a binarization routine (adaptive thresholding or Otsu) and add tests in `test_ocr.py`.
- Consider adding unit tests for the preprocessing pipeline and a small example image in `data/sample/` for CI testing.


