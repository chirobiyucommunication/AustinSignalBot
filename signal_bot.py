# ==============================
# AUSTIN SIGNAL SERVER
# Receives signals and stores them
# ==============================

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# ---------------- CONFIG ----------------

# >>> DO NOT CHANGE THIS
SIGNAL_LOG = "signals.json"


# ---------------- DATABASE ----------------

def load_signals():
    # >>> Loads saved signals
    if os.path.exists(SIGNAL_LOG):
        with open(SIGNAL_LOG, "r") as f:
            return json.load(f)
    return []

def save_signals(data):
    # >>> Saves signals to file
    with open(SIGNAL_LOG, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- TEST ROUTE ----------------
# >>> When you open your render link in browser,
# >>> this prevents "Not Found" error

@app.route("/", methods=["GET"])
def home():
    return "Austin Signal Bot is LIVE"


# ---------------- SIGNAL ENDPOINT ----------------
# >>> THIS is where TradingView / AI / Telegram will send signals

@app.route("/signal", methods=["POST"])
def receive_signal():
    data = request.json

    # >>> REQUIRED SIGNAL FORMAT
    required = ["pair", "direction", "timeframe", "strength"]

    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    if not all(field in data for field in required):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    # >>> Save signal
    signals = load_signals()
    signals.append(data)
    save_signals(signals)

    print("NEW SIGNAL:", data)

    return jsonify({"status": "success", "message": "Signal received"}), 200


# ---------------- GET LAST SIGNAL ----------------
# >>> Client bot will use this later

@app.route("/latest", methods=["GET"])
def latest_signal():
    signals = load_signals()

    if not signals:
        return jsonify({"status": "empty"})

    return jsonify(signals[-1])


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    print("Signal bot running...")
    app.run(host="0.0.0.0", port=5001)
