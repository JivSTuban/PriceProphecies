import streamlit as st

st.set_page_config(
    page_title='PriceProphecies', # Set the page title
    page_icon=':money_with_wings:', # This is an emoji shortcode. Could be a URL too.
)
st.write('PriceProphecies is a powerful tool for tracking and predicting stock prices. Use our tracker to monitor real-time stock data and our predictions to forecast future price movements.')

st.header('Features')
st.write('''
- **Real-time Stock Tracking**: Monitor stock prices in real-time.
- **Price Predictions**: Get accurate predictions for future stock prices.
- **User-friendly Interface**: Easy to use with a clean and intuitive design.
''')

st.header('Getting Started')
st.write('''
1. Navigate to the **Tracker** page to start monitoring stock prices.
2. Use the **Predictions** page to get price forecasts.
3. Explore the app and discover its full potential!
''')

st.header('Contact Us')
st.write('If you have any questions or feedback, feel free to reach out to us at jivtuban14@gmail.com.')