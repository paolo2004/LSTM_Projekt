from _datetime import datetime
import json
import pandas as pd
import requests  # to send HTTP requests
import streamlit as st
from bs4 import BeautifulSoup  # for parsing HTML and XML documents

st.set_page_config(page_title="IPO Dashboard", layout="wide")
st.title("📊 Upcoming IPO Dashboard")

# # def get_yahoo_ipos():
# #     try:
# #         url = "https://finance.yahoo.com/calendar/ipo"
# #         headers = {
# #             "User-Agent": (
# #                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
# #                 "AppleWebKit/537.36 (KHTML, like Gecko) "
# #                 "Chrome/120.0.0.0 Safari/537.36"
# #             )
# #         }
# #
# #         r = requests.get(url, headers=headers, timeout=10)
# #         r.raise_for_status()
# #
# #         return pd.read_html(r.text)[0]
# #
# #     except Exception as e:
# #         st.warning("Yahoo IPO data temporarily unavailable (rate limited).")
# #         return pd.DataFrame()
#

def get_stockanalysis_ipo():
    url = "https://stockanalysis.com/ipos/calendar/"
    headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
    }
    r = requests.get(url, headers=headers, timeout=10)
    return pd.read_html(r.text)[0]

def get_nasdaq_ipo():
    url = "https://api.nasdaq.com/api/ipo/calendar"
    #url = "https://www.nasdaq.com/market-activity/ipos"
    headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
    }
    r = requests.get(url, headers=headers)
    #r.raise_for_status()

    response_json = r.json()
    st.write(response_json)

    data = r.json()["data"]["upcoming"]["upcomingTable"]["rows"]

    today = datetime.today().date()
    ipos = []

    for row in data:
        try:
            ipo_date = datetime.strptime(row["expectedPriceDate"], "%m/%d/%y").date()
        except Exception:
            continue

        #if ipo_date > today:
        ipos.append({
                "IPO-Date": ipo_date,
                "Company": row["companyName"],
                "Symbol": row["proposedTickerSymbol", ""],
                "Exchange": row["proposedExchange", ""],
                "Price Range": row["proposedSharePrice", ""],
                "Values of proposed Shares": row["dollarValueOfSharesOffered", ""]
            })

    if not ipos:
        st.warning("Not upcoming Nasdaq IPos")
        return pd.DataFrame()
    return pd.DataFrame(ipos)

def get_investing_ipo():
    url = "https://www.investing.com/ipo-calendar/"
    headers = {"User-Agent": "Mozilla/5.0"} # Set a User-Agent header so the request looks like it comes from a real browser.
    response = requests.get(url, headers=headers)
    #print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")

    ipos = []
    rows = soup.select("table tbody tr")
    today = datetime.today().date()

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 4:
            # Convert string date to datetime object
            try:
                ipo_date = datetime.strptime(cols[0].text.strip(), "%b %d, %Y").date()
            except ValueError:
                continue # skip rows with invalid date

            if ipo_date >= today:
                ipos.append({
                 "IPO Date": cols[0].text.strip(),
                  "Company": cols[1].text.strip(),
                  "Exchange": cols[2].text.strip(),
                  "IPO Value": cols[3].text.strip(),
                  "Price Range": cols[4].text.strip()
            })
    if not ipos:
        st.warning("No IPO data available.")
        return pd.DataFrame()

    return pd.DataFrame(ipos)

def get_marketwatch_ipo():
    url = "https://www.marketwatch.com/tools/ipo-calendar"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # will raise clear error if blocked

    tables = pd.read_html(response.text)
    return tables[1]  # or whichever table you need

source = st.selectbox(
    "Select IPO Data Source",
    ["Nasdaq", "StockAnalysis", "Investing.com", "MarketWatch"]
)

@st.cache_data
def load_data(source):
    if source == "StockAnalysis":
        return get_stockanalysis_ipo()
    elif source == "Nasdaq":
        return get_nasdaq_ipo()
    elif source == "Investing.com":
        return get_investing_ipo()
    elif source == "MarketWatch":
        return get_marketwatch_ipo()

df = load_data(source)

st.subheader(f"Upcoming IPO - {source}")
st.dataframe(df, use_container_width=True)