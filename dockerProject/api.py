from flask import Flask, jsonify, abort
import json
import os

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    if not os.path.exists('scraped_data.json'):
        abort(404, description="File not found")
    try:
        with open('scraped_data.json', 'r') as file:
            data = [json.loads(line) for line in file]
        return jsonify(data)
    except json.JSONDecodeError:
        abort(500, description="Error decoding JSON")

if __name__ == '__main__':
    app.run(debug=True)
