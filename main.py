from datetime import datetime
import pdfplumber
import re
import difflib

from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

import os
from dotenv import load_dotenv

# Load environmental variables (for secrets)
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Temp placeholder; replace with pdf route
PDF_ROUTE = "./test.pdf"

# Backend legacy method
auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
client = BackendApplicationClient(client_id=CLIENT_ID)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url="https://api.sharesight.com/oauth2/token", auth=auth)

# Detect portfolio id
port_resp = oauth.get("https://api.sharesight.com/api/v2/portfolios.json")
port_resp.raise_for_status()
portfolio_id = port_resp.json()["portfolios"][0]["id"]

# Get list of existing trades for given portfolio
trades_resp = oauth.get(f"https://api.sharesight.com/api/v2/portfolios/{portfolio_id}/trades.json")
trades_resp.raise_for_status()
trades = trades_resp.json()["trades"]

inst_resp = oauth.get("https://api.sharesight.com/api/v2/user_instruments.json")
inst_resp.raise_for_status()
instruments = {item["name"]: item["id"] for item in inst_resp.json()["instruments"]}


def process_tranasction_desc(description, instruments):
    match_key = difflib.get_close_matches(description, instruments.keys(), n=1)[0]
    return instruments[match_key]


# Intialise variables
KEEP_PAGE = False
TRADE_PARAMS = [
    "transaction_date",
    "transaction_type",
    "instrument_id",
    "quantity",
    "price",
    "brokerage_currency_code",
    "exchange_rate",
    "value"
]

# Initalise recorders
all_lines = []
new_trades = []

with pdfplumber.open("./test2.pdf") as pdf:
    for page in pdf.pages:
        page_lines = page.extract_text().split("\n")
        KEEP_PAGE = KEEP_PAGE or ("Transactions" in page_lines)
        if KEEP_PAGE and ("Notes" not in page_lines):
            all_lines.extend(page_lines)

for line in all_lines:
    line_values = line.split(" ")
    if len(line_values) == len(TRADE_PARAMS):
        try:
            line_values[0] = (
                datetime.
                strptime(line_values[0], "%d%b%Y").
                date().
                isoformat()
            )
        except ValueError:
            continue
        else:
            if line_values[1] != "Dividend":
                line_values[1] = "BUY"
                line_values[2] = process_tranasction_desc(line_values[2], instruments)
                line_values[3] = float(line_values[3])
                line_values[4] = float(line_values[4])
                line_values[6] = float(line_values[6])
                line_values[7] = float(line_values[7])
                new_trades.append(dict(zip(TRADE_PARAMS, line_values)))

for trade in new_trades:
    if not any([all([tr[k] == v for k, v in trade.items()]) for tr in trades]):
        trade["portfolio_id"] = portfolio_id
        post_resp = oauth.post("https://api.sharesight.com/api/v2/trades.json", json={"trade": trade})
        post_resp.raise_for_status()