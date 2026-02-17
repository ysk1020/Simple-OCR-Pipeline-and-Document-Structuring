import argparse
from pathlib import Path

from PIL import Image

from src.ocr.tesseract_engine import run_ocr
from src.export.to_json import save_json
from src.export.to_csv import save_csv  # <- make sure your file has this
from src.visualize.annotate import  save_annotated_image  # <- make sure your file has this

def iter_images(input_dir: Path):
    if input_dir.is_file():
        yield input_dir
        return
    
    exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    for p in sorted(input_dir.rglob('*')):
        if p.suffix.lower() in exts:
            yield p

def main():
    parser = argparse.ArgumentParser(description="OCR pipeline")
    parser.add_argument('-i','--input', type=Path, required=True, dest='input', help="Input image or directory")
    parser.add_argument('-o','--out','--output', type=Path, default=Path('output'), dest='output', help="Output directory")
    
    args = parser.parse_args()

    input_path = Path(args.input)
    out_root = Path(args.output)
    out_json_dir = out_root / 'tables'
    out_csv_dir = out_root / 'tables'
    out_annotated_dir = out_root / 'annotated_images'

    out_json_dir.mkdir(parents=True, exist_ok=True)
    out_csv_dir.mkdir(parents=True, exist_ok=True)
    out_annotated_dir.mkdir(parents=True, exist_ok=True)
    processed=0

    for img_path in iter_images(input_path):
        print(f"Processing {img_path}...")
        image = Image.open(img_path)
        tokens = run_ocr(image)
        payload = {
            'file':img_path.name,
            'engine':'tesseract',
            'tokens':tokens,
        }
        # Save JSON
        json_path = out_json_dir / img_path.with_suffix('.json').name
        save_json(payload, json_path)

        # Save CSV
        csv_path = out_csv_dir / img_path.with_suffix('.csv').name
        save_csv(tokens, csv_path)

        # Save annotated image
        annotated_name = img_path.stem + '_annotated' + img_path.suffix
        annotated_path = out_annotated_dir / annotated_name
        save_annotated_image(image, tokens, annotated_path)

        print(f"Saved JSON to {json_path}, CSV to {csv_path}, annotated image to {annotated_path}")
        processed+=1
    print(f"Processed {processed} images.")

if __name__ == "__main__":
    main()