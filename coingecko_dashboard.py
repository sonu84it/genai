from flask import Flask, render_template_string
import json
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
    {% if coins %}
    <table>
        <tr>
            {% for key in keys %}
            <th>{{ key }}</th>
            {% endfor %}
        </tr>
        {% for coin in coins %}
        <tr>
            {% for key in keys %}
            <td>{{ coin[key]|tojson if coin[key] is mapping or coin[key] is sequence else coin[key] }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p style="text-align:center;">No data available</p>
    {% endif %}
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

    keys = list(coins[0].keys()) if coins else []

    return render_template_string(TEMPLATE, coins=coins, keys=keys)


if __name__ == "__main__":
    app.run(debug=True)
