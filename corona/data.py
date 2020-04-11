import time
import datetime

import pickle
import requests
from pathlib import Path


def _write_cache(data, cache_file):
    if not cache_file.parent.is_dir():
        cache_file.parent.mkdir()

    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)

def _read_cache(cache_file):
    with open(cache_file, 'rb') as f:
        data = pickle.load(f)
    return data

def download_if_not_updated(url="https://api.covid19india.org/data.json",
                           cache_file=Path("/tmp/corona_india_data/corona.pkl")):
    def update():
        data = requests.get(url).json()
        _write_cache(data, cache_file)
        return data

    if not cache_file.is_file():
        data = update()
        return data

    f_time = cache_file.stat().st_mtime
    date = datetime.datetime.fromtimestamp(f_time).strftime("%D")

    if date != datetime.datetime.now().strftime("%D"):
        data = update()
        return data

    data = _read_cache(cache_file)

    return data

def delete_cache(cache_file=Path("/tmp/corona_india_data/corona.pkl")):
    cache_file.unlink()
    
