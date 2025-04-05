import pandas as pd
import yaml

from utils.consts import CONFIG_PATH


def extract_excel(uni_dataset_path: str = None):
    if uni_dataset_path:
        path = uni_dataset_path
    else:
        with open(CONFIG_PATH, 'r') as f:
            cfg = yaml.safe_load(f)

            uni_settings = cfg['uni_dataset']
            path = uni_settings["path"]
    df = pd.read_excel(path)
    return df