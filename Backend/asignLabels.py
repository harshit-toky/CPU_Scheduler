# import json 
# from process_scheduling1 import fcfs_scheduling, sjf_preemptive, round_robin_scheduling, priority_preemptive

# # Load the raw scheduling tables
# with open("./cpu_scheduling_random_tables.json", "r") as f:
#     data = json.load(f)

# # List to store processed output
# final_dataset = []
# fcfs, sjf, rr, priority = 0,0,0,0

# for i in data:
#     table_id = i["table_id"]
#     processes = i["processes"]
#     time_quantum = i["time_quantum"]

#     process_table = []
#     id = 1
#     for process in processes:
#         process_table.append({
#             "id": id,
#             "arrivalTime": process[0],
#             "burstTime": process[1],
#             "priority": process[2]
#         })
#         id += 1

#     # Run all scheduling algorithms
#     _, fcfs_tat, fcfs_wt, fcfs_gantt_log = fcfs_scheduling(process_table)
#     _, sjf_tat, sjf_wt, sjf_gantt_log = sjf_preemptive(process_table)
#     _, rr_tat, rr_wt, rr_gantt_log = round_robin_scheduling(process_table, time_quantum)
#     _, priority_tat, priority_wt, priority_gantt_log = priority_preemptive(process_table)

#     # Store soft metrics
#     soft_metrics = {
#         "FCFS": {"avg_tat": fcfs_tat, "avg_wt": fcfs_wt},
#         "SJF": {"avg_tat": sjf_tat, "avg_wt": sjf_wt},
#         "RR": {"avg_tat": rr_tat, "avg_wt": rr_wt},
#         "Priority": {"avg_tat": priority_tat, "avg_wt": priority_wt}
#     }

#     # Compute best algorithm (lowest TAT + WT)
#     combined_scores = {k: v["avg_tat"] + v["avg_wt"] for k, v in soft_metrics.items()}
#     best_algo = min(combined_scores, key=combined_scores.get)
#     if(best_algo == "FCFS"):
#         fcfs += 1
#     elif best_algo == 'SJF':
#         sjf+=1
#     elif best_algo == 'RR':
#         rr += 1
#     else : 
#         priority += 1
#     # Final dataset entry
#     entry = {
#         "table_id": table_id,
#         "processes": processes,
#         "time_quantum": time_quantum,
#         "soft_metrics": soft_metrics,
#         "best_algo": best_algo
#     }

#     final_dataset.append(entry)
#     # print(table_id ," Done")

# print("FCFS :", fcfs )
# print("SJF :", sjf)
# print("Round Robin :", rr)
# print("Priority :", priority)
# # Write to output JSON
# with open("labeled_scheduling_dataset.json", "w") as f:
#     json.dump(final_dataset, f, indent=2)

# print("✅ Dataset saved as labeled_scheduling_dataset.json")
import json
from process_scheduling1 import fcfs_scheduling, sjf_preemptive, round_robin_scheduling, priority_preemptive
from collections import defaultdict
import math

def analyze_gantt_log(gantt_log, process_info):
    stats = defaultdict(lambda: {"starts": [], "ends": [], "total_burst": 0})

    for entry in gantt_log:
        pid = entry["id"]
        start = entry["start"]
        end = entry["end"]

        stats[pid]["starts"].append(start)
        stats[pid]["ends"].append(end)
        stats[pid]["total_burst"] += end - start

    metrics = {}
    starvation_threshold = 20
    for pid, times in stats.items():
        arrival = process_info[pid]["arrivalTime"]
        burst = process_info[pid]["burstTime"]
        priority = process_info[pid]["priority"]
        first_start = min(times["starts"])
        completion = max(times["ends"])
        turnaround = completion - arrival
        waiting = turnaround - burst
        response = first_start - arrival
        starved = int(response > starvation_threshold)

        metrics[pid] = {
            "arrival": arrival,
            "burst": burst,
            "priority": priority,
            "start_time": first_start,
            "completion": completion,
            "waiting_time": waiting,
            "turnaround_time": turnaround,
            "response_time": response,
            "starved": starved
        }
    return metrics

def compute_full_metrics(gantt_log, process_table):
    process_info = {p["id"]: p for p in process_table}
    metrics = analyze_gantt_log(gantt_log, process_info)

    n = len(metrics)
    total_wt = total_tat = total_rt = total_starved = 0
    waiting_times = []
    priority_violations = 0

    # Sort gantt log to check priority violations
    gantt_log.sort(key=lambda x: x["start"])
    for i in range(1, len(gantt_log)):
        prev = gantt_log[i - 1]
        curr = gantt_log[i]
        prev_priority = process_info[prev["id"]]["priority"]
        curr_priority = process_info[curr["id"]]["priority"]
        if curr_priority > prev_priority:
            priority_violations += 1

    for pid, m in metrics.items():
        total_wt += m["waiting_time"]
        total_tat += m["turnaround_time"]
        total_rt += m["response_time"]
        total_starved += m["starved"]
        waiting_times.append(m["waiting_time"])

    avg_wt = total_wt / n
    avg_tat = total_tat / n
    avg_rt = total_rt / n
    fairness = round(stat_std(waiting_times), 2)  # lower std dev = fairer

    return {
        "avg_tat": round(avg_tat, 2),
        "avg_wt": round(avg_wt, 2),
        "avg_rt": round(avg_rt, 2),
        "starved": total_starved,
        "fairness": fairness,
        "priority_violations": priority_violations
    }

def stat_std(data):
    if len(data) <= 1:
        return 0.0
    mean = sum(data) / len(data)
    return math.sqrt(sum((x - mean) ** 2 for x in data) / len(data))

def normalize_dict(metric_dict):
    normed = {}
    for key in metric_dict:
        values = [metric_dict[key][m] for m in metric_dict[key]]
        mins = {m: min(metric_dict[k][m] for k in metric_dict) for m in metric_dict[key]}
        maxs = {m: max(metric_dict[k][m] for k in metric_dict) for m in metric_dict[key]}
        normed[key] = {}
        for m in metric_dict[key]:
            min_v = mins[m]
            max_v = maxs[m]
            v = metric_dict[key][m]
            normed[key][m] = 0 if max_v == min_v else (v - min_v) / (max_v - min_v)
    return normed


import os


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "cpu_scheduling_balanced.json")
with open(file_path) as f:
    data = json.load(f)

final_dataset = []
algo_counts = {"FCFS": 0, "SJF": 0, "RR": 0, "Priority": 0}

for i in data:
    table_id = i["table_id"]
    processes = i["processes"]
    time_quantum = i["time_quantum"]

    process_table = [
        {"id": idx + 1, "arrivalTime": p[0], "burstTime": p[1], "priority": p[2]}
        for idx, p in enumerate(processes)
    ]

    # Run algorithms
    _, _, _, fcfs_log = fcfs_scheduling(process_table)
    _, _, _, sjf_log = sjf_preemptive(process_table)
    _, _, _, rr_log = round_robin_scheduling(process_table, time_quantum)
    _, _, _, priority_log = priority_preemptive(process_table)

    # Extract full metrics from Gantt logs
    all_metrics = {
        "FCFS": compute_full_metrics(fcfs_log, process_table),
        "SJF": compute_full_metrics(sjf_log, process_table),
        "RR": compute_full_metrics(rr_log, process_table),
        "Priority": compute_full_metrics(priority_log, process_table)
    }

    # Normalize for fair scoring
    normalized = normalize_dict(all_metrics)

    # Weighted scoring (lower is better)
    weights = {
    "avg_tat": 0.1,
    "avg_wt": 0.1,
    "avg_rt": 0.1,
    "starved": 0.25,
    "fairness": 0.25,
    "priority_violations": 0.25
    }



    scores = {
        algo: sum(normalized[algo][m] * w for m, w in weights.items())
        for algo in all_metrics
    }

    best_algo = min(scores, key=scores.get)
    algo_counts[best_algo] += 1

    final_dataset.append({
        "table_id": table_id,
        "processes": processes,
        "time_quantum": time_quantum,
        "soft_metrics": all_metrics,
        "best_algo": best_algo
    })

# Save final dataset
save_file_path = os.path.join(script_dir, "labeled_scheduling_dataset.json")
with open(save_file_path, "w") as f:
    json.dump(final_dataset, f, indent=2)

# Print summary
for algo, count in algo_counts.items():
    print(f"{algo}: {count}")
print("✅ Full dataset saved to labeled_scheduling_dataset.json")

