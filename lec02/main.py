from flask import Flask, request, jsonify
from job.fetch_sales import fetch_sales_data
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run_job():
    data = request.get_json()
    raw_dir = data.get('raw_dir')
    date = data.get('date')

    if not raw_dir or not date:
        return jsonify({"error": "Missing raw_dir or date parameter"}), 400

    fetch_sales_data(raw_dir, date)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
