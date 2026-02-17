from pathlib import Path
from typing import List, Dict, Union

import cv2
import numpy as np
from PIL import Image

def draw_boxes(image:Image.Image, tokens:List[Dict])->Image.Image:
    # draw rectangle for each bbox
    # return annotated image
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    for token in tokens:
        x1, y1, x2, y2 = token['bbox']
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)

def save_annotated_image(image:Image.Image, tokens:List[Dict], filename:Union[str, Path])->None:
    out_path = Path(filename)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    annotated=draw_boxes(image, tokens)
    annotated.save(out_path)
