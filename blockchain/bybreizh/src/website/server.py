from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "crypto_data.json"

def load_local_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        return {}

@app.route('/')
def index():
    cryptos_data = load_local_data()
    cryptos = []

    for crypto_id, data in cryptos_data.items():
        latest_price = data.get("prices", [[0, "N/A"]])[-1][1]  # Dernier prix connu
        cryptos.append({"id": crypto_id, "name": crypto_id.capitalize(), "price": latest_price})

    return render_template('index.html', cryptos=cryptos)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/crypto/<crypto_id>')
def crypto_page(crypto_id):
    secret_file = request.args.get('secret_file')
    secret_content = None
    
    if secret_file:
        try:
            with open(secret_file, 'r') as f:
                secret_content = f.read()
        except Exception as e:
            secret_content = f"Erreur de lecture : {e}"

    return render_template('crypto.html', crypto_id=crypto_id, secret_content=secret_content)


@app.route('/crypto/<crypto_id>/chart-data')
def crypto_chart_data(crypto_id):
    cryptos_data = load_local_data()
    
    if crypto_id not in cryptos_data:
        return jsonify({"error": "Données indisponibles"}), 404

    prices = cryptos_data[crypto_id].get("prices", [])
    labels = []
    values = []
    
    for point in prices:
        timestamp = point[0] / 1000  # Convertir millisecondes en secondes
        labels.append(datetime.fromtimestamp(timestamp).strftime('%m-%d %H:%M'))
        values.append(point[1])

    return jsonify({"labels": labels, "prices": values})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
