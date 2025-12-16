import streamlit as st
import yfinance as yf
import pandas as pd
st.title("Recent News about a stock")

# USER INPUT
ticker = st.text_input("Enter a Stock Ticker (e.g. AAPL, TSLA, GOOGL)")
#lookback_days = st.slider("Lookback Days", 3, 30, 7)

# NEWS BUTTON
if st.button("Show News"):
    if ticker == "":
        st.warning("Please enter a stock ticker.")
    else:
        try:
            stock = yf.Ticker(ticker)
            st.text(stock.history(period='1d', interval='60m', auto_adjust=False))
            news = stock.news

            if not news or len(news) == 0:
                st.error("No news data available.")
            else:
                # --- CHANGE IS HERE: Convert list of dicts to DataFrame ---
                st.json(news)

                for new in news:
                    i = 1
                    st.subheader(" 🆕 New " +  i)
                    st.write(f"**Title:** {new.get('title', 'N/A')}")
                    st.write(f"**Description:** {new.get('description', 'N/A')}")
                    st.write(f"**Publisher:** {new.get('publisher', 'N/A')}")
                    st.write(f"**Link:** {new.get('link', 'N/A')}")



                news_df = pd.DataFrame(news)

                # Select and rename columns for a cleaner display
                # We also convert the 'providerPublishTime' from timestamp to datetime
                if 'providerPublishTime' in news_df.columns:
                    news_df['Date'] = pd.to_datetime(news_df['providerPublishTime'], unit='s')

                # Create a DataFrame with the most useful columns for display
                display_cols = ['title', 'publisher', 'link', 'Date']

                # Filter the DataFrame to only include columns that exist (in case yfinance changes its format)
                final_df = news_df[[col for col in display_cols if col in news_df.columns]]

                # Display the DataFrame as an interactive table
                st.dataframe(final_df)
        except Exception as e:
            st.error(f"Error fetching news: {e}")