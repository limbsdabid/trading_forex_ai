import MetaTrader5 as mt5

from config_loader import load_config


def main():
    creds = load_config()

    if not mt5.initialize():
        print("Initialization failed, error code =", mt5.last_error())
        return 1

    try:
        authorized = mt5.login(creds["login"], creds["password"], creds["server"])
        if not authorized:
            print("Login failed, error code =", mt5.last_error())
            return 1

        print("Connected to MT5 demo account")

        eurusd = mt5.symbol_info_tick("EURUSD")
        if eurusd:
            print(f"EUR/USD Bid: {eurusd.bid}, Ask: {eurusd.ask}")
        else:
            print("Symbol not found or data unavailable.")
            return 1

        return 0
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
