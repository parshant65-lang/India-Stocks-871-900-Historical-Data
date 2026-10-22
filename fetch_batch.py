import os
import sys
import datetime
import pandas as pd
import yfinance as yf

HEADERS = ["timestamp", "datetime_utc", "open", "high", "low", "close", "volume"]

COMPANIES = {
    "CHEMFAB": ("Chemfab Alkalis Limited", "CHEMFAB.NS"),
    "CHEMPLASTS": ("Chemplast Sanmar Limited", "CHEMPLASTS.NS"),
    "CHEVIOT": ("Cheviot Company Limited", "CHEVIOT.NS"),
    "CIFL": ("Capital India Finance Limited", "CIFL.NS"),
    "CINELINE": ("Cineline India Limited", "CINELINE.NS"),
    "CINEVISTA": ("Cinevista Limited", "CINEVISTA.NS"),
    "CLEDUCATE": ("CL Educate Limited", "CLEDUCATE.NS"),
    "CLSEL": ("Chaman Lal Setia Exports Limited", "CLSEL.NS"),
    "CMLL": ("Caliber Mining and Logistics Limited", "CMLL.NS"),
    "CMRGREEN": ("CMR Green Technologies Limited", "CMRGREEN.NS"),
    "CMSINFO": ("CMS Info Systems Limited", "CMSINFO.NS"),
    "CNL": ("Creative Newtech Limited", "CNL.NS"),
    "COASTCORP": ("Coastal Corporation Limited", "COASTCORP.NS"),
    "COCKERILL": ("John Cockerill India Limited", "COCKERILL.NS"),
    "COFFEEDAY": ("Coffee Day Enterprises Limited", "COFFEEDAY.NS"),
    "COMFINTE": ("Comfort Intech Limited", "COMFINTE.NS"),
    "COMPEAU": ("Competent Automobiles Company Limited", "COMPEAU.NS"),
    "COMPINFO": ("Compuage Infocom Limited", "COMPINFO.NS"),
    "COMPUSOFT": ("Compucom Software Limited", "COMPUSOFT.NS"),
    "COMSYN": ("Commercial Syn Bags Limited", "COMSYN.NS"),
    "CONFIPET": ("Confidence Petroleum India Limited", "CONFIPET.NS"),
    "CONSOFINVT": ("Consolidated Finvest & Holdings Limited", "CONSOFINVT.NS"),
    "CONTROLPR": ("Control Print Limited", "CONTROLPR.NS"),
    "CORALFINAC": ("Coral India Finance & Housing Limited", "CORALFINAC.NS"),
    "CORDELIA": ("Waterways Leisure Tourism Limited", "CORDELIA.NS"),
    "CORDSCABLE": ("Cords Cable Industries Limited", "CORDSCABLE.NS"),
    "CORONA": ("CORONA Remedies Limited", "CORONA.NS"),
    "COSMOFIRST": ("COSMO FIRST LIMITED", "COSMOFIRST.NS"),
    "COUNCODOS": ("Country Condo's Limited", "COUNCODOS.NS"),
    "CPCAP": ("CP Capital Limited", "CPCAP.NS"),
}


def fetch_and_save_company(symbol, company_name, default_ticker):
    print(f"Fetching 1m data for {symbol} ({company_name})...")
    candidates = [
        default_ticker,
        f"{symbol}.NS",
        f"{symbol.replace('&', '-')}.NS",
        f"{symbol.replace('&', '_')}.NS",
        f"{symbol}.BO"
    ]
    df = None
    for cand in candidates:
        try:
            ticker = yf.Ticker(cand)
            cand_df = ticker.history(period="7d", interval="1m")
            if not cand_df.empty:
                df = cand_df
                break
        except Exception:
            continue

    if df is None or df.empty:
        print(f"No data returned for {symbol} across candidates")
        return False, 0

    rows = []
    for idx, row in df.iterrows():
        ts_utc = idx.to_pydatetime()
        if ts_utc.tzinfo is None:
            ts_utc = ts_utc.replace(tzinfo=datetime.timezone.utc)
        else:
            ts_utc = ts_utc.astimezone(datetime.timezone.utc)

        epoch_ms = int(ts_utc.timestamp() * 1000)
        dt_utc_str = ts_utc.strftime("%Y-%m-%d %H:%M:%S")

        raw_vol = row.get("Volume", 0)
        try:
            vol_int = int(round(float(raw_vol))) if pd.notna(raw_vol) else 0
            vol_int = max(0, vol_int)
        except Exception:
            vol_int = 0

        rows.append({
            "timestamp": epoch_ms,
            "datetime_utc": dt_utc_str,
            "open": round(float(row["Open"]), 4),
            "high": round(float(row["High"]), 4),
            "low": round(float(row["Low"]), 4),
            "close": round(float(row["Close"]), 4),
            "volume": vol_int,
            "date_utc": ts_utc.strftime("%Y-%m-%d")
        })

    full_df = pd.DataFrame(rows)
    grouped = full_df.groupby("date_utc")
    total_candles = 0

    for date_str, group in grouped:
        year, month, _ = date_str.split("-")
        folder = os.path.join(symbol, "1m", year, month)
        os.makedirs(folder, exist_ok=True)
        csv_path = os.path.join(folder, f"{symbol}_1m_{date_str}.csv")

        to_write = group[HEADERS].copy()
        to_write["volume"] = pd.to_numeric(to_write["volume"], errors="coerce").fillna(0).astype("int64")
        to_write["timestamp"] = pd.to_numeric(to_write["timestamp"], errors="coerce").astype("int64")

        if os.path.exists(csv_path):
            existing = pd.read_csv(csv_path)
            combined = pd.concat([existing, to_write], ignore_index=True)
            combined = combined.drop_duplicates(subset=["timestamp"], keep="last").sort_values("timestamp")
            combined["volume"] = pd.to_numeric(combined["volume"], errors="coerce").fillna(0).astype("int64")
            combined["timestamp"] = pd.to_numeric(combined["timestamp"], errors="coerce").astype("int64")
            for c in ["open", "high", "low", "close"]:
                if c in combined.columns:
                    combined[c] = combined[c].round(4)
            combined[HEADERS].to_csv(csv_path, index=False)
            total_candles += len(combined)
        else:
            to_write = to_write.sort_values("timestamp")
            to_write[HEADERS].to_csv(csv_path, index=False)
            total_candles += len(to_write)

    return True, total_candles

def sanitize_existing_csvs():
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.endswith(".csv") and "_1m_" in f:
                p = os.path.join(root, f)
                try:
                    df = pd.read_csv(p)
                    if "volume" in df.columns:
                        needs_clean = False
                        if df["volume"].dtype != "int64":
                            needs_clean = True
                        elif df["volume"].astype(str).str.contains(r"\.[0-9]+$", regex=True).any():
                            needs_clean = True
                        
                        if needs_clean:
                            df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0).astype("int64")
                            df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce").astype("int64")
                            for c in ["open", "high", "low", "close"]:
                                if c in df.columns:
                                    df[c] = df[c].round(4)
                            df = df.drop_duplicates(subset=["timestamp"], keep="last").sort_values("timestamp")
                            df[HEADERS].to_csv(p, index=False)
                except Exception:
                    pass

def main():
    print("Starting automated ingestion for batch...")
    sanitize_existing_csvs()
    success_count = 0
    total_candles = 0
    for symbol, (cname, ticker) in COMPANIES.items():
        ok, candles = fetch_and_save_company(symbol, cname, ticker)
        if ok:
            success_count += 1
            total_candles += candles
    print(f"Batch completed: {success_count}/{len(COMPANIES)} companies ingested, {total_candles} candles.")

if __name__ == "__main__":
    main()
