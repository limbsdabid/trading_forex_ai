# Fetch data from all available symbols and save to CSV __________________________________________________________________________________________________
# data_fetch.py
import os
import json
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# load credentials from config.json ____________________________________________________________________________________
with open("config.json") as f:
    cfg = json.load(f)

LOGIN = cfg["login"]
PASSWORD = cfg["password"]
SERVER = cfg["server"]

def initialize_mt5():
    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")
    if not mt5.login(LOGIN, PASSWORD, SERVER):
        raise RuntimeError(f"MT5 login failed: {mt5.last_error()}")

def shutdown_mt5():
    mt5.shutdown()

# Fetch candles for a symbol and timeframe, return as DataFrame _____________________________________________________________________________________________
def fetch_candles(symbol, timeframe=mt5.TIMEFRAME_H1, start=None, end=None):
    rates = mt5.copy_rates_range(symbol, timeframe, start, end)
    if rates is None or len(rates) == 0:
        return pd.DataFrame()
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['symbol'] = symbol
    return df[['symbol','time','open','high','low','close','tick_volume','spread','real_volume']]

def save_or_append(symbol, timeframe_label, new_df):
    filename = os.path.join(DATA_DIR, f"{symbol}_{timeframe_label}.csv")
    if os.path.exists(filename):
        old = pd.read_csv(filename, parse_dates=['time'])
        combined = pd.concat([old, new_df], ignore_index=True)
        combined.drop_duplicates(subset=['symbol','time'], inplace=True)
        combined.sort_values(by='time', inplace=True)
        combined.to_csv(filename, index=False)
        print(f"Appended {len(new_df)} rows to {filename} (now {len(combined)} rows).")
    else:
        new_df.sort_values(by='time', inplace=True)
        new_df.to_csv(filename, index=False)
        print(f"Saved {len(new_df)} rows to new file {filename}.")

# Incrementally update data for a symbol and timeframe
def incremental_update(symbol, timeframe=mt5.TIMEFRAME_H1, timeframe_label="H1", fetch_chunk_days=365):
    filename = os.path.join(DATA_DIR, f"{symbol}_{timeframe_label}.csv")
    if os.path.exists(filename):
        existing = pd.read_csv(filename, parse_dates=['time'])
        last_time = existing['time'].max()
        start_time = last_time + timedelta(seconds=1)
        end_time = datetime.now(timezone.utc)
    else:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=fetch_chunk_days)

    current_start = start_time
    all_new = []
    while current_start < end_time:
        current_end = min(current_start + timedelta(days=fetch_chunk_days), end_time)
        df = fetch_candles(symbol, timeframe, current_start, current_end)
        if not df.empty:
            all_new.append(df)
        current_start = current_end + timedelta(seconds=1)

    if all_new:
        new_df = pd.concat(all_new, ignore_index=True)
        save_or_append(symbol, timeframe_label, new_df)
    else:
        print("No new data fetched.")

if __name__ == "__main__":
    initialize_mt5()
    try:
        symbol = "EURUSD"
        timeframe = mt5.TIMEFRAME_H1
        timeframe_label = "H1"

        start_date = datetime(2018, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2026, 1, 8, tzinfo=timezone.utc)

        df = fetch_candles(
            symbol,
            timeframe=timeframe,
            start=start_date,
            end=end_date
        )

        if df.empty:
            print(f"No data fetched for {symbol}. Check symbol name or MT5 Market Watch.")
        else:
            save_or_append(symbol, timeframe_label, df)

            print("Patch first candle:", df['time'].min())
            print("Patch last candle:", df['time'].max())
            print("Patch rows:", len(df))

    finally:
        shutdown_mt5()
# Fetch data from all available symbols and save to CSV __________________________________________________________________________________________________
# data_fetch.py
import os
import json
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# load credentials from config.json ____________________________________________________________________________________
with open("config.json") as f:
    cfg = json.load(f)

LOGIN = cfg["login"]
PASSWORD = cfg["password"]
SERVER = cfg["server"]

def initialize_mt5():
    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")
    if not mt5.login(LOGIN, PASSWORD, SERVER):
        raise RuntimeError(f"MT5 login failed: {mt5.last_error()}")

def shutdown_mt5():
    mt5.shutdown()

# Fetch candles for a symbol and timeframe, return as DataFrame _____________________________________________________________________________________________
def fetch_candles(symbol, timeframe=mt5.TIMEFRAME_H1, start=None, end=None):
    rates = mt5.copy_rates_range(symbol, timeframe, start, end)
    if rates is None or len(rates) == 0:
        return pd.DataFrame()
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['symbol'] = symbol
    return df[['symbol','time','open','high','low','close','tick_volume','spread','real_volume']]

def save_or_append(symbol, timeframe_label, new_df):
    filename = os.path.join(DATA_DIR, f"{symbol}_{timeframe_label}.csv")
    if os.path.exists(filename):
        old = pd.read_csv(filename, parse_dates=['time'])
        combined = pd.concat([old, new_df], ignore_index=True)
        combined.drop_duplicates(subset=['symbol','time'], inplace=True)
        combined.sort_values(by='time', inplace=True)
        combined.to_csv(filename, index=False)
        print(f"Appended {len(new_df)} rows to {filename} (now {len(combined)} rows).")
    else:
        new_df.sort_values(by='time', inplace=True)
        new_df.to_csv(filename, index=False)
        print(f"Saved {len(new_df)} rows to new file {filename}.")

# Incrementally update data for a symbol and timeframe
def incremental_update(symbol, timeframe=mt5.TIMEFRAME_H1, timeframe_label="H1", fetch_chunk_days=365):
    filename = os.path.join(DATA_DIR, f"{symbol}_{timeframe_label}.csv")
    if os.path.exists(filename):
        existing = pd.read_csv(filename, parse_dates=['time'])
        last_time = existing['time'].max()
        start_time = last_time + timedelta(seconds=1)
        end_time = datetime.now(timezone.utc)
    else:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=fetch_chunk_days)

    current_start = start_time
    all_new = []
    while current_start < end_time:
        current_end = min(current_start + timedelta(days=fetch_chunk_days), end_time)
        df = fetch_candles(symbol, timeframe, current_start, current_end)
        if not df.empty:
            all_new.append(df)
        current_start = current_end + timedelta(seconds=1)

    if all_new:
        new_df = pd.concat(all_new, ignore_index=True)
        save_or_append(symbol, timeframe_label, new_df)
    else:
        print("No new data fetched.")

if __name__ == "__main__":
    initialize_mt5()
    try:
        symbol = "EURUSD"
        timeframe = mt5.TIMEFRAME_H1
        timeframe_label = "H1"

        start_date = datetime(2018, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2026, 6, 8, tzinfo=timezone.utc)

        df = fetch_candles(
            symbol,
            timeframe=timeframe,
            start=start_date,
            end=end_date
        )

        if df.empty:
            print(f"No data fetched for {symbol}. Check symbol name or MT5 Market Watch.")
        else:
            save_or_append(symbol, timeframe_label, df)

            print("Patch first candle:", df['time'].min())
            print("Patch last candle:", df['time'].max())
            print("Patch rows:", len(df))

    finally:
        shutdown_mt5()
