
from typing import List, Dict
import pytesseract
from pytesseract import Output

def run_ocr(image)->List[Dict]:
    ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    results = []
    for i in range(len(ocr_data['text'])): 
        text = ocr_data['text'][i].strip()
        if not text:
            continue
        try: 
            conf = float(ocr_data['conf'][i])
        except (ValueError, TypeError):
            continue

        if conf <= 0:  
            continue

        x = ocr_data['left'][i]
        y = ocr_data['top'][i]
        w = ocr_data['width'][i]
        h = ocr_data['height'][i]

        token={
            'text': text,
            'confidence': conf,
            'bbox': [x, y, x + w, y + h],
            'block_num': ocr_data['block_num'][i],
            'line_num': ocr_data['line_num'][i],
        }

        results.append(token)
    return results