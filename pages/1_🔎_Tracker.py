import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import freecurrencyapi

# Set up the Streamlit app
st.set_page_config(
    page_title='PriceProphecies', # Set the page title
    page_icon=':money_with_wings:', # This is an emoji shortcode. Could be a URL too.
)

# Load environment variables from .env file
load_dotenv()

# Streamlit app title
st.title('Price Tracker 🔎')

# Create placeholder for the chart
chart_placeholder = st.empty()

# Initialize DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['time', 'price', 'asset_id'])

# Initialize selected_asset
if 'selected_asset' not in st.session_state:
    st.session_state.selected_asset = 'BTC'  # Default to Bitcoin

# Ensure selected_asset is defined before using it
selected_asset = st.session_state.selected_asset

# Display the chart for the selected asset
with chart_placeholder.container():
    asset_data = st.session_state.df[st.session_state.df['asset_id'] == st.session_state.selected_asset]

# Add a dropdown menu for selecting the currency
selected_currency = st.selectbox('Select Currency', ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'PHP', 'CAD', 'CHF', 'CNY', 'HKD', 'INR', 'KRW', 'MXN', 'NZD', 'SGD', 'ZAR'])

# Add a flag based on the selected currency
if selected_currency == 'USD':
    flag = '🇺🇸'
elif selected_currency == 'EUR':
    flag = '🇪🇺'
elif selected_currency == 'JPY':
    flag = '🇯🇵'
elif selected_currency == 'GBP':
    flag = '🇬🇧'
elif selected_currency == 'AUD':
    flag = '🇦🇺'
elif selected_currency == 'PHP':
    flag = '🇵🇭'
elif selected_currency == 'CAD':
    flag = '🇨🇦'
elif selected_currency == 'CHF':
    flag = '🇨🇭'
elif selected_currency == 'CNY':
    flag = '🇨🇳'
elif selected_currency == 'HKD':
    flag = '🇭🇰'
elif selected_currency == 'INR':
    flag = '🇮🇳'
elif selected_currency == 'KRW':
    flag = '🇰🇷'
elif selected_currency == 'MXN':
    flag = '🇲🇽'
elif selected_currency == 'NZD':
    flag = '🇳🇿'
elif selected_currency == 'SGD':
    flag = '🇸🇬'
elif selected_currency == 'ZAR':
    flag = '🇿🇦'

# Calculate default dates
latest_date = datetime.now().date()
start_date_default = latest_date - timedelta(days=30)

# Add date input for selecting the time frame side by side
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input('Start Date', start_date_default)
with col2:
    end_date = st.date_input('End Date', latest_date)

# Add a dropdown menu for selecting the period
period_options = {
    '1 min': '1MIN',
    '3 min': '3MIN',
    '5 min': '5MIN',
    '10 min': '10MIN',
    '30 min': '30MIN',
    '1 hour': '1HRS',
    '3 hours': '3HRS',
    '5 hours': '5HRS',
    '12 hours': '12HRS',
    '24 hours': '1DAY',
    '3 days': '3DAY',
    '1 week': '7DAY',
    '1 month': '1MTH'
}
selected_period = st.selectbox('Select Period', list(period_options.keys()), index=5)

# Initialize freecurrencyapi client
client = freecurrencyapi.Client(os.getenv('FREECURRENCYAPI_API_KEY'))

# Fetch historical data for the selected asset, currency, and time frame
def fetch_historical_data(asset, currency, start_date, end_date, period):
    api_key = os.getenv('COINAPI_API_KEY')
    url = f"https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_{asset}_USD/history?period_id={period_options[period]}&time_start={start_date}T00:00:00&time_end={end_date}T23:59:59&limit=10000"
    headers = {
        'X-CoinAPI-Key': api_key
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.SSLError as e:
        st.error(f"SSL Error: {e}")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"Request Error: {e}")
        return pd.DataFrame()

    if not data:
        st.error("No data received from the API.")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    if 'time_period_start' not in df.columns or 'price_open' not in df.columns:
        st.error("Unexpected data structure received from the API.")
        return pd.DataFrame()

    df['time'] = pd.to_datetime(df['time_period_start'])
    df['price'] = df['price_open']
    df['asset_id'] = asset

    # Fetch conversion rate using freecurrencyapi
    conversion_rate = client.latest(currencies=[currency])['data'][currency]
    if conversion_rate is not None:
        df['price'] = df['price'] * conversion_rate

    # Check if the CSV file already exists
    csv_filename = f"data/{asset}-{start_date}-{end_date}.csv"
    if not os.path.exists(csv_filename):
        # Save the data to a CSV file
        df.to_csv(csv_filename, index=False)
    else:
        # Check if the start date is within the date range of the existing file
        existing_files = [f for f in os.listdir('data') if f.startswith(f"{asset}-") and f.endswith('.csv')]
        for file in existing_files:
            parts = file.split('-')
            if len(parts) != 4:
                continue

            file_start_date_str, file_end_date_str = parts[1], parts[2]
            try:
                file_start_date = datetime.strptime(file_start_date_str, '%Y-%m-%d').date()
                file_end_date = datetime.strptime(file_end_date_str, '%Y-%m-%d').date()
            except ValueError:
                try:
                    file_start_date = datetime.strptime(file_start_date_str, '%Y-%m').date()
                    file_end_date = datetime.strptime(file_end_date_str, '%Y-%m').date()
                except ValueError:
                    try:
                        file_start_date = datetime.strptime(file_start_date_str, '%Y').date()
                        file_end_date = datetime.strptime(file_end_date_str, '%Y').date()
                    except ValueError:
                        try:
                            file_start_date = datetime.strptime(file_start_date_str, '%Y-%m-%d-%Y-%m-%d').date()
                            file_end_date = datetime.strptime(file_end_date_str, '%Y-%m-%d-%Y-%m-%d').date()
                        except ValueError:
                            st.error(f"Unexpected date format in file: {file}")
                            continue

            if start_date >= file_start_date and start_date <= file_end_date:
                st.warning(f"Data for {start_date} is already included in {file}")
                return df

        # Save the data to a CSV file
        df.to_csv(csv_filename, index=False)

    return df

# Fetch historical data for the selected asset, currency, and time frame
try:
    st.session_state.df = fetch_historical_data(selected_asset, selected_currency, start_date, end_date, selected_period)
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data for {selected_currency}: {e}")

# Display the chart for the selected asset
with chart_placeholder.container():
    asset_data = st.session_state.df[st.session_state.df['asset_id'] == selected_asset]
    if not asset_data.empty:
        st.subheader(f"{selected_asset} Price in {selected_currency} {flag}")
        st.line_chart(asset_data.set_index('time')['price'])
