from flask import Flask, request, jsonify
from flask_cors import CORS  # To allow React to communicate with Flask
import subprocess
import json
app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        print("Received data:", data)

        # Call gantt_chart.py using subprocess
        process = subprocess.Popen(
            ["python", "process_scheduling.py"],  # Run external script
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Ensures output is returned as a string
        )

        # Send JSON data as input to the script
        stdout, stderr = process.communicate(json.dumps(data))

        if stderr:
            return jsonify({"error": stderr}), 500
        print("Sending Data to React")
        return jsonify({"message": "Gantt Chart Generated", "chart": stdout.strip()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)