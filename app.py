from flask import Flask, request, jsonify
from flask_cors import CORS  # To allow React to communicate with Flask

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()  # Get JSON data from React
        print("Received data:", data)  # Print to check in backend
        return jsonify({"message": "Data received successfully!", "data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask server
