import json
import numpy as np
import joblib
from process_scheduling1 import fcfs_scheduling, sjf_preemptive, round_robin_scheduling, priority_preemptive
import os
import pandas as pd
from AIUsingGPT import generate_why_explanation

def extract_features(processes, tq=4):
    arrivals = [p["arrivalTime"] for p in processes]
    bursts = [p["burstTime"] for p in processes]
    prios = [p["priority"] for p in processes]

    return {
        "num_processes": len(processes),
        "avg_arrival": np.mean(arrivals),
        "std_arrival": np.std(arrivals),
        "avg_burst": np.mean(bursts),
        "std_burst": np.std(bursts),
        "max_burst": np.max(bursts),
        "min_burst": np.min(bursts),
        "avg_priority": np.mean(prios),
        "std_priority": np.std(prios),
        "max_priority": np.max(prios),
        "min_priority": np.min(prios),
        "arrival_span": max(arrivals) - min(arrivals),
        "time_quantum": tq
    }

def compute_metrics(gantt_log, processes):
    id_to_process = {p["id"]: p for p in processes}
    finish_times = {}
    first_response = {}
    start_times = {}

    for log in gantt_log:
        pid = log["id"]
        start = log["start"]
        end = log["end"]

        if pid not in first_response:
            first_response[pid] = start

        finish_times[pid] = end
        if pid not in start_times:
            start_times[pid] = start

    n = len(processes)
    tats = []
    wts = []
    rts = []
    priority_violations = 0

    for p in processes:
        pid = p["id"]
        at = p["arrivalTime"]
        bt = p["burstTime"]
        pr = p["priority"]
        ft = finish_times[pid]
        rt = first_response[pid]

        tat = ft - at
        wt = tat - bt
        response = rt - at

        tats.append(tat)
        wts.append(wt)
        rts.append(response)

    fairness = max(wts) - min(wts)
    starved = sum(1 for wt in wts if wt > 2 * np.mean(wts))
    priority_violations = sum(1 for log in gantt_log if id_to_process[log["id"]]["priority"] != min(p["priority"] for p in processes if p["arrivalTime"] <= log["start"]))

    return {
        "avg_tat": round(np.mean(tats), 2),
        "avg_wt": round(np.mean(wts), 2),
        "avg_rt": round(np.mean(rts), 2),
        "starved": starved,
        "fairness": round(fairness, 2),
        "priority_violations": priority_violations
    }

def evaluate_algorithms(processes):
    # Try RR with multiple time quantums
    rr_metrics_by_tq = {}
    for tq in range(2, 6):
        _, _, _, rr_gantt = round_robin_scheduling(processes, tq)
        rr_metrics_by_tq[tq] = compute_metrics(rr_gantt, processes)

    best_rr_tq = min(rr_metrics_by_tq, key=lambda k: rr_metrics_by_tq[k]["avg_tat"] + rr_metrics_by_tq[k]["avg_wt"])
    best_rr_metrics = rr_metrics_by_tq[best_rr_tq]

    _, _, _, fcfs_gantt = fcfs_scheduling(processes)
    _, _, _, sjf_gantt = sjf_preemptive(processes)
    _, _, _, prio_gantt = priority_preemptive(processes)

    return {
        "FCFS": compute_metrics(fcfs_gantt, processes),
        "SJF": compute_metrics(sjf_gantt, processes),
        "RR": best_rr_metrics,
        "Priority": compute_metrics(prio_gantt, processes)
    }, best_rr_tq

def predict_best_algo(processes):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "best_algo_predictor_model.pkl")
    model = joblib.load(file_path)
    best_metrics, best_rr_tq = evaluate_algorithms(processes)

    features = extract_features(processes, tq=best_rr_tq)
    input_df = pd.DataFrame([features])
    pred = model.predict(input_df)[0]
    algo_map = {0: "FCFS", 1: "SJF", 2: "RR", 3: "Priority"}
    explanation = generate_why_explanation(algo_map[pred], best_metrics) 
    # print(explanation)
    return {
        "predicted_best_algo": algo_map[pred],
        "soft_metrics": best_metrics,
        "best_time_quantum_if_rr": best_rr_tq if algo_map[pred] == "RR" else None,
        "explanation" : explanation
    }

# Usage
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "processes.json")
with open(file_path) as f:
    data = json.load(f)

result = predict_best_algo(data)

print(json.dumps(result, indent=2))
