import json
import matplotlib.pyplot as plt
import sys
import io
import base64


def fcfs_scheduling(processes):
    processes = sorted(processes, key=lambda x: x['arrivalTime'])
    time = 0
    gantt_log = []
    for p in processes:
        start = max(time, p['arrivalTime'])
        end = start + p['burstTime']
        p['completion_time'] = end
        p['turnaround_time'] = end - p['arrivalTime']
        p['waiting_time'] = p['turnaround_time'] - p['burstTime']
        gantt_log.append({'id': p['id'], 'start': start, 'end': end})
        time = end
    avg_tat = sum(p['turnaround_time'] for p in processes) / len(processes)
    avg_wt = sum(p['waiting_time'] for p in processes) / len(processes)
    return processes, avg_tat, avg_wt, gantt_log


def sjf_preemptive(processes):
    n = len(processes)
    remaining = [p['burstTime'] for p in processes]
    initial_burst = [p['burstTime'] for p in processes]
    complete = 0
    time = 0
    minm = float('inf')
    shortest = -1
    check = False
    gantt_log = []
    prev = -1

    # Track total executed time per process
    executed_time = {p['id']: 0 for p in processes}
    segment_executed = 0  # tracks time in the current segment

    while complete != n:
        for i in range(n):
            if (processes[i]['arrivalTime'] <= time and
                    remaining[i] < minm and remaining[i] > 0):
                minm = remaining[i]
                shortest = i
                check = True

        if not check:
            time += 1
            continue

        process_id = processes[shortest]['id']

        # Detect context switch
        if prev != shortest:
            if gantt_log and 'end' not in gantt_log[-1]:
                gantt_log[-1]['end'] = time
            gantt_log.append({
                'id': process_id,
                'start': time
            })
            segment_executed = 0  # reset for new segment
            prev = shortest

        # Execute 1 unit of time
        remaining[shortest] -= 1
        executed_time[process_id] += 1
        segment_executed += 1
        time += 1

        # Percent complete for this segment
        percent = (segment_executed / initial_burst[shortest]) * 100
        gantt_log[-1]['percent_complete'] = round(percent, 2)

        if remaining[shortest] == 0:
            complete += 1
            finish_time = time
            processes[shortest]['completion_time'] = finish_time
            processes[shortest]['turnaround_time'] = finish_time - processes[shortest]['arrivalTime']
            processes[shortest]['waiting_time'] = processes[shortest]['turnaround_time'] - processes[shortest]['burstTime']
            gantt_log[-1]['end'] = finish_time

        minm = float('inf')
        check = False

    if gantt_log and 'end' not in gantt_log[-1]:
        gantt_log[-1]['end'] = time

    avg_tat = sum(p['turnaround_time'] for p in processes) / n
    avg_wt = sum(p['waiting_time'] for p in processes) / n
    return processes, avg_tat, avg_wt, gantt_log







def priority_preemptive(processes):
    time = 0
    complete = 0
    n = len(processes)
    remaining = [p['burstTime'] for p in processes]
    burst_time = [p['burstTime'] for p in processes]
    executed_time = {p['id']: 0 for p in processes}
    gantt_log = []
    prev = -1
    segment_executed = 0

    while complete != n:
        available = [i for i in range(n) if processes[i]['arrivalTime'] <= time and remaining[i] > 0]
        if not available:
            time += 1
            continue

        # Assuming lower numerical value = higher priority
        highest_priority = min(available, key=lambda x: processes[x]['priority'])
        current_id = processes[highest_priority]['id']

        # Detect context switch
        if prev != highest_priority:
            if gantt_log and 'end' not in gantt_log[-1]:
                gantt_log[-1]['end'] = time
            gantt_log.append({'id': current_id, 'start': time})
            segment_executed = 0
            prev = highest_priority

        # Execute for 1 unit
        remaining[highest_priority] -= 1
        executed_time[current_id] += 1
        segment_executed += 1
        time += 1

        # Update percentage for current segment
        percent = (segment_executed / burst_time[highest_priority]) * 100
        gantt_log[-1]['percent_complete'] = round(percent, 2)

        if remaining[highest_priority] == 0:
            complete += 1
            finish_time = time
            processes[highest_priority]['completion_time'] = finish_time
            processes[highest_priority]['turnaround_time'] = finish_time - processes[highest_priority]['arrivalTime']
            processes[highest_priority]['waiting_time'] = processes[highest_priority]['turnaround_time'] - processes[highest_priority]['burstTime']
            gantt_log[-1]['end'] = finish_time

    # Close any remaining gantt block
    if gantt_log and 'end' not in gantt_log[-1]:
        gantt_log[-1]['end'] = time

    avg_tat = sum(p['turnaround_time'] for p in processes) / n
    avg_wt = sum(p['waiting_time'] for p in processes) / n
    return processes, avg_tat, avg_wt, gantt_log




def round_robin_scheduling(processes, time_quantum):
    queue = []
    time = 0
    remaining = {p['id']: p['burstTime'] for p in processes}
    burst_time = {p['id']: p['burstTime'] for p in processes}
    p_map = {p['id']: p for p in processes}

    processes.sort(key=lambda x: x['arrivalTime'])
    i = 0
    gantt_log = []
    last_id = -1

    while i < len(processes) or queue:
        while i < len(processes) and processes[i]['arrivalTime'] <= time:
            queue.append(processes[i]['id'])
            i += 1

        if not queue:
            time += 1
            continue

        current = queue.pop(0)

        if last_id != current:
            if gantt_log and 'end' not in gantt_log[-1]:
                gantt_log[-1]['end'] = time
                # Also add percent for previous block
                prev_id = gantt_log[-1]['id']
                seg_duration = gantt_log[-1]['end'] - gantt_log[-1]['start']
                gantt_log[-1]['percent_complete'] = round((seg_duration / burst_time[prev_id]) * 100, 2)

            gantt_log.append({'id': current, 'start': time})
            last_id = current

        exec_time = min(time_quantum, remaining[current])
        remaining[current] -= exec_time
        time += exec_time

        # End this segment
        gantt_log[-1]['end'] = time
        seg_duration = gantt_log[-1]['end'] - gantt_log[-1]['start']
        gantt_log[-1]['percent_complete'] = round((seg_duration / burst_time[current]) * 100, 2)

        while i < len(processes) and processes[i]['arrivalTime'] <= time:
            queue.append(processes[i]['id'])
            i += 1

        if remaining[current] > 0:
            queue.append(current)
        else:
            p = p_map[current]
            p['completion_time'] = time
            p['turnaround_time'] = time - p['arrivalTime']
            p['waiting_time'] = p['turnaround_time'] - p['burstTime']

    avg_tat = sum(p['turnaround_time'] for p in processes) / len(processes)
    avg_wt = sum(p['waiting_time'] for p in processes) / len(processes)

    return processes, avg_tat, avg_wt, gantt_log




def draw_gantt_chart(gantt_log):
    fig, ax = plt.subplots(figsize=(12, 2))
    for entry in gantt_log:
        start = entry['start']
        end = entry['end']
        pid = entry['id']
        ax.barh(0, end - start, left=start, height=0.5, color='skyblue', edgecolor='black')
        ax.text((start + end) / 2, 0, f"P{pid}", ha='center', va='center', fontsize=10, color='black')
    ax.set_xlabel("Time")
    ax.set_yticks([])
    ax.set_xlim(0, max(e['end'] for e in gantt_log))
    ax.set_xticks(range(0, max(e['end'] for e in gantt_log)+1))
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def main():
    with open('processes.json', 'r') as f:
        processes = json.load(f)

    for p in processes:
        p['id'] = int(p['id'])
        p['arrivalTime'] = int(p['arrivalTime'])
        p['burstTime'] = int(p['burstTime'])
        if 'priority' in p:
            p['priority'] = int(p['priority'])

    algorithms = {
        # "FCFS": fcfs_scheduling,
        # "SJF (Preemptive)": sjf_preemptive,
        # "Priority (Preemptive)": priority_preemptive,
        "Round Robin": lambda p: round_robin_scheduling(p, time_quantum=2)
    }

    for name, algo in algorithms.items():
        print(f"\n{name} Scheduling")
        input_copy = json.loads(json.dumps(processes))  # Deep copy
        result, avg_tat, avg_wt, gantt_log = algo(input_copy)
        print("ID  Arrival  Burst  Completion  TAT  WT")
        for p in result:
            print(f"{p['id']:3} {p['arrivalTime']:7} {p['burstTime']:5} {p['completion_time']:10} {p['turnaround_time']:4} {p['waiting_time']:3}")
        print(f"Average Turnaround Time: {avg_tat:.2f}")
        print(f"Average Waiting Time: {avg_wt:.2f}")
        filename = f"gantt_{name.lower().replace(' ', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(gantt_log, f, indent=4)
            draw_gantt_chart(gantt_log)


if __name__ == "__main__":
    main()
