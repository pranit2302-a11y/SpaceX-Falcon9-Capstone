import requests
from pathlib import Path

URL = "https://raw.githubusercontent.com/suzushi-tw/IBM_appliend_DS_Capstone/main/dataset_part_1.csv"
OUT = Path("data/dataset_part_1.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)
r = requests.get(URL, timeout=30)
r.raise_for_status()
OUT.write_bytes(r.content)
print(f"Downloaded {OUT} ({len(r.content):,} bytes)")
