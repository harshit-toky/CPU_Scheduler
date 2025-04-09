from flask import Flask, request, jsonify
from flask_cors import CORS  # To allow React to communicate with Flask
import json
from process_scheduling1 import fcfs_scheduling, sjf_preemptive, priority_preemptive, round_robin_scheduling

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        print("Received data:", data)

        # Call gantt_chart.py using subprocess
        # process = subprocess.Popen(
        #     ["python", "process_scheduling.py"],  # Run external script
        #     stdin=subprocess.PIPE,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE,
        #     text=True  # Ensures output is returned as a string
        # )

        # Send JSON data as input to the script
        # stdout, stderr = process.communicate(json.dumps(data))

        # if stderr:
        #     return jsonify({"error": stderr}), 500
        for process in data :
            process["id"] = int(process["id"])
            process["arrivalTime"] = int(process["arrivalTime"])
            process["burstTime"] = int(process["burstTime"])
            process["priority"] = int(process["priority"])
        with open("processes.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Data Received SUccefully")
        return jsonify({"message": "Data Received Successfuly"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

def load_processes_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
@app.route('/fcfs_scheduling', methods=['GET'])
def send_fcfs_ganttLog():
    try:
        processes = load_processes_from_json('processes.json')
        process, avg_tat, avg_wt, gantt_log = fcfs_scheduling(processes)
        return jsonify(gantt_log), 200
    except Exception as e:
        print(e)
        return jsonify({"error" : str(e)}), 400
@app.route('/sjf_scheduling', methods=['GET'])
def send_sjf_ganttLog():
    try:
        processes = load_processes_from_json('processes.json')
        process, avg_tat, avg_wt, gantt_log = sjf_preemptive(processes)
        return jsonify(gantt_log), 200
    except Exception as e:
        print(e)
        return jsonify({"error" : str(e)}), 400
@app.route('/priority_scheduling', methods=['GET'])
def send_priority_ganttLog():
    try:
        processes = load_processes_from_json('processes.json')
        process, avg_tat, avg_wt, gantt_log = priority_preemptive(processes)
        return jsonify(gantt_log), 200
    except Exception as e:
        print(e)
        return jsonify({"error" : str(e)}), 400
@app.route('/roundRobin_scheduling', methods=['GET'])
def send_roundRobin_ganttLog():
    try:
        time_quantum = request.args.get('timeQuantum', type=int)
        processes = load_processes_from_json('processes.json')
        process, avg_tat, avg_wt, gantt_log = round_robin_scheduling(processes, time_quantum)
        return jsonify(gantt_log), 200
    except Exception as e:
        print(e)
        return jsonify({"error" : str(e)}), 400
if __name__ == '__main__':
    app.run(debug=True)