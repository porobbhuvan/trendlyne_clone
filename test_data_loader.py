# test_data_loader.py

from data_loader import get_bhavcopy_symbols

def test_bhavcopy_fetch():
    try:
        symbols = get_bhavcopy_symbols()
        print(f"✅ Successfully fetched {len(symbols)} symbols.")
        print("🔍 First 10 symbols:")
        print(symbols[:10])
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_bhavcopy_fetch()
