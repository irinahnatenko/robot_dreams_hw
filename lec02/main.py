from flask import Flask, request, jsonify
from job.fetch_sales import fetch_sales_data

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run_job():
    data = request.get_json()
    page = data.get("page")
    date = data.get("date")
    raw_dir = data.get("raw_dir")

    if not raw_dir or not date or not page:
        return jsonify({"error": "Missing raw_dir, page, or date parameter"}), 400

    if fetch_sales_data(page, date, raw_dir) is None:
        return jsonify({"error": "Failed to fetch sales data"}), 500

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

