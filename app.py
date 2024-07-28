from flask import Flask, render_template, jsonify
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    data = []
    with open('btc_usdt_1hour.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row['Time']
            open_price = float(row['Open'])
            high = float(row['High'])
            low = float(row['Low'])
            close = float(row['Close'])
            timestamp = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp() * 1000
            data.append([timestamp, open_price, high, low, close])
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
