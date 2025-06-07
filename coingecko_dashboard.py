from flask import Flask, render_template_string
import requests

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CoinGecko Top Coins</title>
    <style>
        table { border-collapse: collapse; width: 60%; margin: auto; }
        th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
        th { background-color: #f5f5f5; }
    </style>
</head>
<body>
    <h2 style="text-align:center;">Top {{ coins|length }} Cryptocurrencies</h2>
    <table>
        <tr><th>Rank</th><th>Name</th><th>Price (USD)</th></tr>
        {% for coin in coins %}
        <tr>
            <td>{{ coin.market_cap_rank }}</td>
            <td>{{ coin.name }}</td>
            <td>${{ "{:,.2f}".format(coin.current_price) }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''


def fetch_top_coins(limit=10):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": "false",
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


@app.route("/")
def index():
    try:
        coins = fetch_top_coins()
    except requests.RequestException as exc:
        coins = []
        print(f"Error fetching data: {exc}")
    return render_template_string(TEMPLATE, coins=coins)


if __name__ == "__main__":
    app.run(debug=True)
