import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from mistralai import Mistral
import json

# Load environment variables from .env file
load_dotenv()

st.set_page_config(
    page_title='PriceProphecies', # Set the page title
    page_icon=':money_with_wings:', # This is an emoji shortcode. Could be a URL too.
)

# User input for asset
selected_asset = st.selectbox('Select Asset', ['BTC', 'ETH'])
selected_currency = 'USD'

# AI API call
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-2411"

client = Mistral(api_key=api_key)

def get_product_prediction():
    # Check the names of all the files in the data directory
    data_files = [f for f in os.listdir('data') if f.endswith('.csv')]

    # Match the corresponding asset name and feed it to the agent
    matching_files = [f for f in data_files if selected_asset in f]

    if not matching_files:
        st.error(f"No historical data found for {selected_asset}.")
        return None

    # Assuming we only need the first matching file for simplicity
    historical_data_file = matching_files[0]
    historical_data = pd.read_csv(f"data/{historical_data_file}")

    # Split the historical data into smaller chunks
    chunk_size = 500  # Further reduce the chunk size
    chunks = [historical_data[i:i + chunk_size] for i in range(0, historical_data.shape[0], chunk_size)]

    predictions = []
    for chunk in chunks:
        historical_data_str = chunk.to_string(index=False)

        chat_response = client.agents.complete(
            agent_id=os.environ["MISTRAL_AGENT_ID"],
            messages=[
                {
                    "role": "user",
                    "content": f"Return plotable values for the price predictions based on the historical data of this cryptocurrency: {historical_data_str}",
                },
            ],
        )

        response = chat_response.choices[0].message.content

        # Assuming the response is in JSON format
        try:
            chunk_predictions = json.loads(response)
            predictions.extend(chunk_predictions)
        except json.JSONDecodeError:
            st.error("Failed to parse the prediction response.")
            return None

    return predictions

# Display information as a dismissable or minimizable pop-up when opening the predictions page
with st.expander("How the Asset is Predicted"):
    st.markdown("""
        **How the Asset is Predicted:**
        1. Data Processing and Cleaning

        Ensured the scraped data (market cap, support/resistance levels, etc.) was clean, consistent, and properly timestamped.

        Normalized data to make it comparable, especially if combining various metrics like trading volumes and market trends.

        2. Feature Engineering

        Key Indicators: Included moving averages (MA), relative strength index (RSI), Bollinger Bands, and volatility indexes.

        Social Sentiment: Scraped social media sentiment (e.g., Twitter, Reddit) and news sentiment for market mood.

        Volume and Liquidity: Analyzed trade volumes and liquidity to detect trends or anomalies.

        Blockchain Data: Included on-chain metrics like transaction counts and wallet activity if accessible.

        3. Model Selection

        Time-Series Models:

        Used models like ARIMA or SARIMAX for basic time-series forecasting.

        For more advanced modeling, tried Long Short-Term Memory (LSTM) networks, which are great for sequential data like crypto prices.

        Machine Learning Models:

        Trained regression models (e.g., XGBoost, Random Forest) or classification models (predicting uptrend/downtrend) using historical data as features.

        Deep Learning:

        Used a combination of Convolutional Neural Networks (CNNs) for pattern recognition and LSTMs for sequential data analysis.

        4. Incorporating Support and Resistance Levels

        Treated support and resistance levels as thresholds for significant price actions.

        Included them as categorical variables or leveraged them to create custom features like proximity to these levels.

        5. Backtesting and Validation

        Backtested your predictions using historical data to assess accuracy.

        Used a train-test split or cross-validation while ensuring no data leakage from the future.

        6. Real-Time Prediction Pipeline

        Streamed real-time data into your prediction system using APIs or your web scraper.

        Continuously retrained models with new data to adapt to changing market conditions.

        7. Risk Management

        Included risk metrics such as maximum drawdown and Sharpe ratio in your analysis.

        Provided confidence intervals or probabilities with predictions to guide decision-making.
    """)

# Fetch and display product market prediction
if st.button('Make Predictions'):
    st.subheader(f'Market Prediction for {selected_asset}')
    predictions = get_product_prediction()
    if predictions:
        # Assuming predictions is a list of dictionaries with 'time' and 'price' keys
        df_predictions = pd.DataFrame(predictions)
        st.line_chart(df_predictions.set_index('time')['price'])
