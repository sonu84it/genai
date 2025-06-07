# genai

## CoinGecko UI Examples

This repository contains example scripts that fetch data from the [CoinGecko](https://www.coingecko.com/) API.
One example uses Tkinter to display data in a desktop window and another serves a simple dashboard using Flask.

### Tkinter example

1. Ensure Python 3 and the `requests` library are available:

   ```bash
   pip install requests
   ```

2. Run the script:

   ```bash
   python3 coingecko_ui.py
   ```

A window will open showing the rank, name and current price of the top cryptocurrencies.

### Flask dashboard

Install the required library if you haven't already:

```bash
pip install flask
```

Start the web server:

```bash
python3 coingecko_dashboard.py
```

Open `http://localhost:5000` in your browser to see the treemap of top coins.
