import signal
from time import sleep
from dhanhq_ticker_py import (
    DhanTicker,
    get_option_chain,
    get_expiry_dates,
    get_instruments_details,
)

login_id = "Paste Your User User Id / Login Id Here"
password = "Paste Your User Password Here"
# Or You Can Read From A Plain Text File / Config / TOML / YAML Files.


# Define The Callbacks / Method Hooks
def on_ticks(tick):
    print(tick, end="\n" * 2)


def on_order_update(order_update):
    print(order_update, end="\n" * 2)


# Assign The Callbacks / Method Hooks

callbacks = DhanTicker.default_callbacks().update(
    {"on_tick": on_ticks, "on_order_update": on_order_update}
)

ticker = DhanTicker(
    callbacks=callbacks,
    # debug=False, # Uncomment This For Debugging
    # debug_verbose=False, # Uncomment This For Verbose Debugging
)

ticker.login_with_credentials(login_id, password)

# As Dhan Doesnt Offer Provisions To Use TOTP, Instead It Send OTP On
# The Registered Mobile Number And Email ID. The Program Will Wait For
# The User To Key In The Received OTP In The Terminal / Console And Press
# Enter To Continue Completing A Successfull Login With Credentials.

# Fetch Instrument Details For Which We Want To Subscribe For Market Data
bnf_expiry, nf_expiry = [get_expiry_dates(idx, "NSE") for idx in {"BANKNIFTY", "NIFTY"}]
nearest_bnf_expiry, nearest_nf_expiry = (
    bnf_expiry["ExpiryDate"][0],
    nf_expiry["ExpiryDate"][0],
)

instruments = get_instruments_details(
    ["NIFTY", "BANKNIFTY"],
    "NSE",
    is_optidx=True,
    expiry_dates=[nearest_bnf_expiry, nearest_nf_expiry],
    strikes=[20000, 45000],
    opt_types=["CE", "PE"],
)
finnifty_all_nearest_expiry_options = get_option_chain("FINNIFTY", "NSE")

# Subscribe / Unsubscribe To The Instruments, It Can Be At Any Point
# After Instantiation of `DhanTicker` Class Object With Either `userdata`
# Or Login With Credentials.

# There Are Only Two Modes, Quote Mode and Full Mode.

if instruments is not None:
    ticker.subscribe(instruments, mode=ticker.FULL)
ticker.subscribe(finnifty_all_nearest_expiry_options, mode=ticker.FULL)


# The Ticker is fully asynchronous and runs in a backgroung thread event loop.
# So We Need To Keep The Main Thread Alive.

if __name__ == "__main__":
    signal.signal(signal.SIGINT, ticker._handle_stop_signals)
    signal.signal(signal.SIGTERM, ticker._handle_stop_signals)

    while True:
        try:
            # Do Any Operation In This Thread, And It Wont
            # Effect The Market Data Feed And Order Update Feed.

            # Or If You do not want to do any operation but only
            # want the updateds to keep printing in the console /
            # terminal, then print anything or put `pass` in this
            # block and keep the rest lines as is.

            print("Dr June Moone Say's Hi! From Main Thread")
        except KeyboardInterrupt:
            break
        else:
            sleep(5)
