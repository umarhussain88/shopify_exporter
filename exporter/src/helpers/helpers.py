import pandas as pd
from pathlib import Path


def get_newest_file(path: Path, ext: str) -> Path:

    file_d = {
        file: pd.to_datetime(file.stat().st_mtime, unit='s')
        for file in path.glob(f'*.{ext}')
    }
    return max(file_d, key=file_d.get)


def create_file_timestamp() -> str:
    return pd.Timestamp('today').strftime('%Y%m%d_%H%M%S')

