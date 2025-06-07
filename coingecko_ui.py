import requests
import tkinter as tk
from tkinter import ttk, messagebox


def fetch_top_coins(limit=10):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": "false",
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def main():
    root = tk.Tk()
    root.title("CoinGecko Top Coins")

    tree = ttk.Treeview(root, columns=("rank", "name", "price"), show="headings")
    tree.heading("rank", text="Rank")
    tree.heading("name", text="Name")
    tree.heading("price", text="Price (USD)")
    tree.pack(fill=tk.BOTH, expand=True)

    try:
        coins = fetch_top_coins()
        for coin in coins:
            tree.insert("", tk.END, values=(coin["market_cap_rank"], coin["name"], f"${coin['current_price']:,}"))
    except requests.RequestException as exc:
        messagebox.showerror("Error", f"Failed to load data: {exc}")

    root.mainloop()


if __name__ == "__main__":
    main()
