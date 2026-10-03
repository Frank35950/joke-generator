from __future__ import annotations

import requests
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

JOKE_URL = (
    "https://v2.jokeapi.dev/joke/Any"
    "?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
    "&type=single"
)


def fetch_joke() -> str:
    response = requests.get(JOKE_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("type") == "single":
        return data.get("joke", "No joke available right now.")

    setup = data.get("setup", "")
    delivery = data.get("delivery", "")
    return f"{setup} {delivery}".strip()


@app.route("/")
def home():
    joke = fetch_joke()

    return render_template_string(
        """
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8" />
            <title>Random Joke Generator</title>
            <style>
              :root {
                --bg: #f6f7fb;
                --panel: #ffffff;
                --ink: #1f2937;
                --muted: #6b7280;
                --brand: #2563eb;
                --shadow: rgba(15, 23, 42, 0.08);
              }
              * { box-sizing: border-box; }
              body {
                margin: 0;
                min-height: 100vh;
                display: grid;
                place-items: center;
                background: linear-gradient(135deg, #eef6ff, #f6f7fb);
                font-family: Arial, sans-serif;
                color: var(--ink);
              }
              .card {
                width: min(680px, 90vw);
                background: var(--panel);
                border-radius: 18px;
                box-shadow: 0 18px 45px var(--shadow);
                padding: 32px 28px;
                text-align: center;
              }
              h1 {
                margin-top: 0;
                font-size: 2rem;
              }
              .joke {
                margin: 24px 0;
                font-size: 1.2rem;
                line-height: 1.7;
                color: var(--ink);
                min-height: 80px;
              }
              button {
                background: var(--brand);
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 10px;
                font-size: 1rem;
                font-weight: 700;
                cursor: pointer;
              }
              button:hover {
                opacity: 0.96;
              }
            </style>
          </head>
          <body>
            <div class="card">
              <h1>Random Joke Generator</h1>
              <div class="joke">{{ joke }}</div>
              <form method="get" action="/">
                <button type="submit">Get another joke</button>
              </form>
            </div>
          </body>
        </html>
        """,
        joke=joke,
    )


@app.route("/api/joke")
def api_joke():
    return jsonify({"joke": fetch_joke()})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
