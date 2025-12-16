import streamlit as st
import yfinance as yf
st.title("Stock Description")

# USER INPUT
ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, GOOGL)")
#lookback_days = st.slider("Lookback Days", 3, 30, 7)

# Description BUTTON
if st.button("Description"):
    if ticker == "":
        st.warning("Please enter a stock ticker.")
        st.stop()
    else:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            #st.json(info)

            st.header(f"🏢 {info.get('longName', ticker.upper())}") # get(key): return the value of the key

            # --- Quick Overview ---"

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Industry:** {info.get('industry', 'N/A')}")
                st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                st.write(f"**Employees:** {info.get('fullTimeEmployees', 'N/A')}")
                st.write(f"**CEO:** {info.get('companyOfficers', [{'name': 'N/A'}])[0].get('name', 'N/A')}")

            with col2:
                # Format Market Cap nicely
                market_cap = info.get("marketCap", None)
                if market_cap:
                    if market_cap >= 1e12:
                        market_cap = f"{market_cap / 1e12:.2f} T USD"
                    elif market_cap >= 1e9:
                        market_cap = f"{market_cap / 1e9:.2f} B USD"
                    elif market_cap >= 1e6:
                        market_cap = f"{market_cap / 1e6:.2f} M USD"
                else:
                    market_cap = "N/A"

                st.write(f"**Market Cap:** {market_cap}")

                div_yield = info.get("dividendYield", None)
                if div_yield:
                    div_yield = f"{div_yield * 100:.2f}%"
                else:
                    div_yield = "N/A"
                st.write(f"**Dividend Yield:** {div_yield}")

                st.write(f"**Website:** [{info.get('website', 'N/A')}]({info.get('website', '')})")

            st.markdown("---")

            # --- Business Summary ---
            st.subheader("📝 Business Summary")
            st.write(info.get("longBusinessSummary", "No business summary available."))

            st.markdown("---")

            # --- Location ---
            st.subheader("📍 Headquarters")
            address = f"""
                    {info.get('address1', '')}
                    {info.get('city', '')}, {info.get('state', '')} {info.get('zip', '')}
                    {info.get('country', '')}
                    """
            st.write(address)

        except Exception as e:
            st.error(f"Error fetching Description: {e}")

