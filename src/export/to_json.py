import json
from pathlib import Path
from typing import Union

def save_json(data:dict, filename:Union[str, Path])->None:
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filename,'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)