import json
import pandas as pd
import yaml

from etl import IExtractor
from utils.consts import CONFIG_PATH


class JsonExtractor(IExtractor):
    def extract(self) -> dict[str, pd.DataFrame]:
        with open(CONFIG_PATH, 'r') as f:
            cfg = yaml.safe_load(f)
            json_settings = cfg['json']
            path = json_settings["path"]

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        rows = []
        for degree_level, studies in data.items():
            for kierunek, details in studies.items():
                row = {
                    'stopien': degree_level,
                    'kierunek': kierunek,
                    **details
                }
                rows.append(row)

        df = pd.DataFrame(rows)
        return {"json_uni_data": df}
        