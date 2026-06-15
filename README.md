# Trading Forex AI

Early-stage AI forex trading bot project. The current baseline connects to MetaTrader 5, verifies account access, and fetches historical candle data for research.

## Current project stage

- MT5 demo connection check: started
- Historical EURUSD H1 candle fetch: started
- Feature engineering: not built yet
- ML training pipeline: not built yet
- Backtesting: not built yet
- Live execution and risk controls: not built yet

## Setup

Install Python 3.12, then rebuild the virtual environment from the project root:

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create your local config file:

```powershell
Copy-Item config.example.json config.json
```

Then edit `config.json` with your MT5 demo login, password, and server. `config.json` is intentionally ignored by git.

## Run

Check MT5 login and live EURUSD tick:

```powershell
python main.py
```

Fetch historical EURUSD H1 candles:

```powershell
python -m data.data_fetch
```

CSV data is written under `data/` and ignored by git.

## Notes for the next development phase

The next clean milestone is to turn the collected candles into a repeatable research pipeline:

- generate features from OHLCV data
- create future-return labels
- train a baseline model
- evaluate with walk-forward validation
- backtest with spread, slippage, and risk limits before any live trading
