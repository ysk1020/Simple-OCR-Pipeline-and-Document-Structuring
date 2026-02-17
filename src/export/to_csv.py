import csv
from pathlib import Path
from typing import List, Dict, Union

def save_csv(tokens:List[Dict], filename:Union[str, Path])->None:
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = [  "text",
        "conf",
        "x1",
        "y1",
        "x2",
        "y2",
        "block_num",
        "line_num"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for token in tokens:
            x1, y1, x2, y2 = token['bbox']
            writer.writerow({
                'text': token['text'],
                'conf': token['confidence'],
                'x1': x1,  
                'y1': y1,
                'x2': x2,   
                'y2': y2,
                'block_num': token['block_num'],
                'line_num': token['line_num']
            })