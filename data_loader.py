# nse_bhavcopy_downloader.py

import pandas as pd
import requests
import zipfile
import io
from datetime import datetime, timedelta

def get_bhavcopy_symbols():
    today = datetime.today()
    target_date = today if today.hour > 17 else today - timedelta(days=1)

    dd = target_date.strftime("%d")
    mon = target_date.strftime("%b").upper()
    yyyy = target_date.strftime("%Y")

    url = f"https://www.nseindia.com/content/historical/EQUITIES/{yyyy}/{mon}/cm{dd}{mon}{yyyy}bhav.csv.zip"
    print(f"Downloading bhavcopy from: {url}")

    # Setup headers and session
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml",
        "Referer": "https://www.nseindia.com/"
    }
    session.headers.update(headers)

    # Set cookies manually to bypass simple anti-bot blocks
    session.get("https://www.nseindia.com", timeout=5)

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            csv_name = z.namelist()[0]
            df = pd.read_csv(z.open(csv_name))
            symbols = df["SYMBOL"].unique().tolist()
            symbols = [s.strip() + ".NS" for s in symbols]
            return symbols

    except requests.exceptions.RequestException as e:
        raise Exception(f"❌ Network error: {e}")
    except zipfile.BadZipFile:
        raise Exception("❌ File is not a valid zip. NSE may be blocking or file not yet available.")
    except Exception as e:
        raise Exception(f"❌ Unknown error: {e}")

if __name__ == "__main__":
    symbols = get_bhavcopy_symbols()
    print(f"✅ Fetched {len(symbols)} symbols.")
    print("🔍 Sample:", symbols[:10])
