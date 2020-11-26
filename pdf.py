from datetime import datetime
import pdfplumber


# Intialise variables
KEEP_PAGE = False
TRADE_PARAMS = [
    "transaction_date",
    "transaction_type",
    "fund_description",
    "quantity",
    "price",
    "brokerage_currency_code",
    "exchange_rate",
    "value"
]

# Initalise recorders
all_lines = []
all_trades = []

with pdfplumber.open("./test.pdf") as pdf:
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
            all_trades.append(dict(zip(TRADE_PARAMS, line_values)))

print(all_trades)
