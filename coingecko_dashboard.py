from flask import Flask, render_template_string
import json
from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import urlencode

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Crypto Market Treemap</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; }
        #treemap { width: 90vw; height: 90vh; margin: auto; }
    </style>
</head>
<body>
    <h2 style="text-align:center;">Top {{ coins|length }} Cryptocurrencies by Market Cap</h2>
    <div id="treemap"></div>
    <script>
        const coins = {{ coins|tojson }};
        function getColor(pct) {
            if (pct === null || pct === undefined || isNaN(pct)) return '#d3d3d3';
            const abs = Math.abs(pct);
            let tone = 'dark';
            if (abs < 5) tone = 'light';
            else if (abs < 10) tone = 'medium';
            const greens = {light: '#b6f2b6', medium: '#5ec25e', dark: '#006400'};
            const reds = {light: '#f7bdbd', medium: '#f06d6d', dark: '#8b0000'};
            return pct >= 0 ? greens[tone] : reds[tone];
        }
        const labels = coins.map(c => (c.symbol.toUpperCase() + ' - ' + c.name));
        const values = coins.map(c => c.market_cap);
        const colors = coins.map(c => getColor(c.price_change_percentage_24h));
        const data = [{
            type: 'treemap',
            labels: labels,
            parents: Array(labels.length).fill(''),
            values: values,
            textinfo: 'label',
            marker: {colors: colors}
        }];
        Plotly.newPlot('treemap', data, {margin: {t: 0, l: 0, r: 0, b: 0}});
    </script>
</body>
</html>
'''


def fetch_top_coins(limit=10):
    """Return market data for the top ``limit`` cryptocurrencies."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": "false",
    }
    query = urlencode(params)
    try:
        with urlopen(f"{url}?{query}", timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except URLError as exc:
        raise RuntimeError(f"Failed to fetch data: {exc}") from exc
    return data


@app.route("/")
def index():
    try:
        coins = fetch_top_coins()
    except Exception as exc:
        coins = []
        print(f"Error fetching data: {exc}")

    return render_template_string(TEMPLATE, coins=coins)


if __name__ == "__main__":
    app.run(debug=True)
