# Binance WebSocket Data Collector

This project collects real-time candlestick data for the Bitcoin to USDT trading pair (`btcusdt`) using Binance's WebSocket API. The data is stored in a Pandas DataFrame, which captures the Open, High, Low, Close prices, and Volume for 1-second intervals.

## Prerequisites

To run this code, you need to have Python installed on your machine along with the following libraries:

- `websocket-client`: For WebSocket connections.
- `pandas`: For handling and manipulating data.
- `json`: For parsing JSON data.
- `datetime`: For handling date and time.

You can install the required libraries using pip:

```bash
pip install websocket-client pandas

