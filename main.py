import MetaTrader5 as mt5
import json

# Load login details from config file ____________________________________________________________________________________
with open("config.json") as f:
    creds = json.load(f)

# Initialize connection
if not mt5.initialize():
    print("Initialization failed, error code =", mt5.last_error())
    quit()

# Attempt login
authorized = mt5.login(creds["login"], creds["password"], creds["server"])
if authorized:
    print("✅ Connected to Vantage demo account")
else:
    print("❌ Login failed, error code =", mt5.last_error())

# Fetch EUR/USD tick data ________________________________________________________________________
eurusd = mt5.symbol_info_tick("EURUSD")
if eurusd:
    print(f"EUR/USD Bid: {eurusd.bid}, Ask: {eurusd.ask}")
else:
    print("Symbol not found or data unavailable.")

# Close connection
mt5.shutdown()
