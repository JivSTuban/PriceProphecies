# :earth_americas: PriceProphecies

PriceProphecies is a powerful tool for tracking and predicting stock prices. Use our tracker to monitor real-time stock data and our predictions to forecast future price movements.

## Project Structure

The project is organized as follows:

- `0_🏠_Home.py`: The main entry point for the Streamlit app.
- `pages/1_🔎_Tracker.py`: Contains the code for tracking stock prices.
- `pages/2_🧪_Predictions.py`: Contains the code for predicting stock prices.
- `data/`: Directory containing historical data files.
- `requirements.txt`: Lists the project dependencies.
- `.env`: Environment variables for API keys.
- `.gitignore`: Specifies files and directories to ignore in version control.
- `LICENSE`: The project license.

## Features

- **Real-time Stock Tracking**: Monitor stock prices in real-time.
- **Price Predictions**: Get accurate predictions for future stock prices.
- **User-friendly Interface**: Easy to use with a clean and intuitive design.

## How to Run

1. Create a virtual environment and activate it:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the app:
    ```bash
    streamlit run 0_🏠_Home.py
    ```

## API Keys

This project uses the following API keys:
- `FREECURRENCYAPI_API_KEY`: API key for FreeCurrencyAPI
- `COINAPI_API_KEY`: API key for CoinAPI
- `MISTRAL_API_KEY`: API key for Mistral AI
- `MISTRAL_AGENT_ID`: Agent ID for Mistral AI

To use the project, you need to create a `.env` file in the root directory with the following content:
```
FREECURRENCYAPI_API_KEY=your_freecurrencyapi_api_key
COINAPI_API_KEY=your_coinapi_api_key
MISTRAL_API_KEY=your_mistral_api_key
MISTRAL_AGENT_ID=your_mistral_agent_id
```

## Tracker Functionality

The tracker page allows you to monitor stock prices in real-time. You can select the asset, currency, and time frame to view historical data.

### Key Features:
- **Real-time Data**: Fetch and display real-time stock data.
- **Currency Conversion**: Convert stock prices to different currencies.
- **Time Frame Selection**: Select the start and end dates for the data.
- **Period Selection**: Choose the period for the data (e.g., 1 hour, 1 day, 1 week).

## Predictions Functionality

The predictions page provides accurate predictions for future stock prices using historical data and AI models.

### Key Features:
- **Historical Data**: Fetch historical data from the `data` directory.
- **AI Predictions**: Use Mistral AI to generate price predictions.
- **Visualization**: Display predictions as a line chart.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
