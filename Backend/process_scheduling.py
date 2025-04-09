import json
import matplotlib.pyplot as plt
import sys
import io
import base64

def fcfs_scheduling(processes):
    # Sort processes by arrival time
    for process in processes:
        process['id'] = int(process['id'])
        process['arrivalTime'] = int(process['arrivalTime'])  # Convert to integer
        process['burstTime'] = int(process['burstTime'])  # Convert to integer
        process['priority'] = int(process['priority'])  # Convert to integer

    processes.sort(key=lambda x: x['arrivalTime'])
    
    completion_time = []
    turnaround_time = []
    waiting_time = []
    
    start_time = 0
    for process in processes:
        if start_time < process['arrivalTime']:
            start_time = process['arrivalTime']
        
        comp_time = start_time + process['burstTime']
        tat = comp_time - process['arrivalTime']
        wt = tat - process['burstTime']
        
        completion_time.append(comp_time)
        turnaround_time.append(tat)
        waiting_time.append(wt)
        
        start_time = comp_time
        
        process['completion_time'] = comp_time
        process['turnaround_time'] = tat
        process['waiting_time'] = wt
    
    avg_tat = sum(turnaround_time) / len(turnaround_time)
    avg_wt = sum(waiting_time) / len(waiting_time)
    
    return processes, avg_tat, avg_wt

def sjf_scheduling_preemptive(processes):
    for process in processes:
        process['id'] = int(process['id'])
        process['arrivalTime'] = int(process['arrivalTime'])
        process['burstTime'] = int(process['burstTime'])
        process['remaining_time'] = process['burstTime']

    time = 0
    completed = []
    ready_queue = []
    gantt_log = []
    current = None

    processes.sort(key=lambda x: x['arrivalTime'])

    while processes or ready_queue or current:
        while processes and processes[0]['arrivalTime'] <= time:
            ready_queue.append(processes.pop(0))

        if current:
            ready_queue.append(current)
            current = None

        if ready_queue:
            ready_queue.sort(key=lambda x: x['remaining_time'])
            current = ready_queue.pop(0)

            # Execute for 1 unit
            start = time
            time += 1
            current['remaining_time'] -= 1
            gantt_log.append({'id': current['id'], 'start': start, 'end': time})

            if current['remaining_time'] == 0:
                current['completion_time'] = time
                current['turnaround_time'] = time - current['arrivalTime']
                current['waiting_time'] = current['turnaround_time'] - current['burstTime']
                completed.append(current)
                current = None
        else:
            time += 1

    # Merge same-process execution segments
    merged = []
    for entry in gantt_log:
        if merged and merged[-1]['id'] == entry['id'] and merged[-1]['end'] == entry['start']:
            merged[-1]['end'] = entry['end']
        else:
            merged.append(entry)

    avg_tat = sum(p['turnaround_time'] for p in completed) / len(completed)
    avg_wt = sum(p['waiting_time'] for p in completed) / len(completed)

    return completed, avg_tat, avg_wt, merged




def priority_scheduling(processes):
    for process in processes:
        process['id'] = int(process['id'])
        process['arrivalTime'] = int(process['arrivalTime'])
        process['burstTime'] = int(process['burstTime'])
        process['priority'] = int(process['priority'])

    time = 0
    completed = []
    waiting_list = []

    while processes or waiting_list:
        waiting_list.extend([p for p in processes if p['arrivalTime'] <= time])
        processes = [p for p in processes if p['arrivalTime'] > time]

        if waiting_list:
            waiting_list.sort(key=lambda x: x['priority'])
            current = waiting_list.pop(0)
            start = time
            time += current['burstTime']
            current['completion_time'] = time
            current['turnaround_time'] = time - current['arrivalTime']
            current['waiting_time'] = current['turnaround_time'] - current['burstTime']
            completed.append(current)
        else:
            time += 1

    avg_tat = sum(p['turnaround_time'] for p in completed) / len(completed)
    avg_wt = sum(p['waiting_time'] for p in completed) / len(completed)

    return completed, avg_tat, avg_wt


def round_robin_scheduling(processes, time_quantum):
    for process in processes:
        process['id'] = int(process['id'])
        process['arrivalTime'] = int(process['arrivalTime'])
        process['burstTime'] = int(process['burstTime'])
        process['remaining_time'] = process['burstTime']

    time = 0
    queue = []
    completed = []
    gantt_log = []
    last_pid = -1
    processes.sort(key=lambda x: x['arrivalTime'])

    while processes or queue:
        while processes and processes[0]['arrivalTime'] <= time:
            queue.append(processes.pop(0))

        if queue:
            current = queue.pop(0)
            start = time
            exec_time = min(time_quantum, current['remaining_time'])
            time += exec_time
            current['remaining_time'] -= exec_time
            gantt_log.append({'id': current['id'], 'start': start, 'end': time})

            while processes and processes[0]['arrivalTime'] <= time:
                queue.append(processes.pop(0))

            if current['remaining_time'] > 0:
                queue.append(current)
            else:
                current['completion_time'] = time
                current['turnaround_time'] = time - current['arrivalTime']
                current['waiting_time'] = current['turnaround_time'] - current['burstTime']
                completed.append(current)
        else:
            time += 1

def draw_gantt_chart(processes):
    fig, ax = plt.subplots(figsize=(10, 4))

    process_names = []
    start_times = []
    burst_times = []

    for process in processes:
        process_names.append(f"P{process['id']}")
        start_times.append(process['completion_time'] - process['burstTime'])
        burst_times.append(process['burstTime'])

    # Plot Gantt chart
    ax.barh(process_names, burst_times, left=start_times, height=0.5, color='skyblue', edgecolor='black')

    # Label each bar with start time and end time
    for i, process in enumerate(processes):
        start = start_times[i]
        end = start + burst_times[i]
        ax.text(start + burst_times[i] / 2, i, f"{start}-{end}", ha='center', va='center', fontsize=10, color='black')

    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart for FCFS Scheduling")
    ax.invert_yaxis()  # To display in order of execution
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

def draw_gantt_chart_single_row(processes):
    fig, ax = plt.subplots(figsize=(12, 2))
    
    start_time = 0
    for process in processes:
        start = process['completion_time'] - process['burstTime']
        end = process['completion_time']
        
        # Draw a bar from start to end
        ax.barh(0, end - start, left=start, height=0.5, color='skyblue', edgecolor='black')
        
        # Place process name inside the bar
        ax.text((start + end) / 2, 0, f"P{process['id']}", ha='center', va='center', fontsize=10, color='black')

    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart for FCFS Scheduling (Single Row)")
    ax.set_yticks([])  # Hide y-axis labels
    ax.set_xticks(range(0, max(p['completion_time'] for p in processes) + 1))  # Show time scale
    ax.set_xlim(0, max(p['completion_time'] for p in processes))
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    # plt.show()
    
    # Convert plot to Base64
    img_io = io.BytesIO()
    plt.savefig(img_io, format="png")
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
    
    plt.close(fig)  # Close the figure to prevent memory leaks
    # print("Sending File...")
    return img_base64


def main():
    # Load process data from JSON file
    with open('processes.json', 'r') as file:
        processes = json.load(file)
    
    scheduled_processes, avg_tat, avg_wt = fcfs_scheduling(processes)
    
    # Display results
    print("Process Schedule:")
    print("ID  Arrival  Burst  Completion  TAT  WT")
    for p in scheduled_processes:
        print(f"{p['id']:3} {p['arrivalTime']:7} {p['burstTime']:5} {p['completion_time']:10} {p['turnaround_time']:4} {p['waiting_time']:3}")
    
    print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
    print(f"Average Waiting Time: {avg_wt:.2f}")

    draw_gantt_chart(scheduled_processes)
    draw_gantt_chart_single_row(scheduled_processes)
    
if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    # with open('processes.json', 'r') as file:
    #     processes = json.load(file)
    # main()
    scheduled_processes, avg_tat, avg_wt = fcfs_scheduling(input_data)
    result = draw_gantt_chart_single_row(scheduled_processes)
    # scheduled_processes, avg_tat, avg_wt, merged = sjf_scheduling_preemptive(processes)
    # result = draw_gantt_chart(scheduled_processes)
    print(result)
