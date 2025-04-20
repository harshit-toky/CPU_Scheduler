# # import random
# # import csv
# # import json
# # from typing import List, Dict, Union

# # def generate_processes(table_type: str, num_processes: int) -> List[List[int]]:
# #     if table_type == 'A':  # SJF (mixed short/long bursts)
# #         bursts = [1, 1, 2, 2, 3, 5, 8, 10]  # Fewer extreme shorts
# #         return [
# #             [random.randint(0, 10), random.choice(bursts), random.randint(1, 10)]
# #             for _ in range(num_processes)
# #         ]
    
# #     elif table_type == 'B':  # RR (clustered arrivals + mixed bursts)
# #         cluster_time = random.randint(0, 5)
# #         bursts = [2, 3, 5, 5, 8, 10, 15]
# #         return [
# #             [max(0, cluster_time + random.randint(-1, 1)), random.choice(bursts), random.randint(3, 7)]
# #             for _ in range(num_processes)
# #         ]
    
# #     elif table_type == 'C':  # Priority (one priority=0 + sparse arrivals)
# #         high_prio_idx = random.randint(0, num_processes-1)
# #         return [
# #             [random.randint(0, 20), random.randint(1, 10), 0 if i == high_prio_idx else random.randint(5, 10)]
# #             for i in range(num_processes)
# #         ]
    
# #     elif table_type == 'D':  # FCFS (long bursts + all at t=0)
# #         base_burst = random.randint(15, 30)
# #         return [
# #             [0, base_burst + random.randint(-2, 2), 5]
# #             for _ in range(num_processes)
# #         ]

# # def generate_time_quantum(table_type: str) -> int:
# #     # All tables get a quantum (even FCFS, though unused)
# #     return random.randint(2, 5)  # Uniform range for fairness

# # def generate_dataset() -> List[Dict]:
# #     dataset = []
# #     # Random weights: 40% SJF, 30% RR, 20% Priority, 10% FCFS
# #     type_weights = [0.4, 0.3, 0.2, 0.1]
    
# #     for table_id in range(1, 1001):
# #         table_type = random.choice(['A', 'B', 'C', 'D'])
# #         num_processes = random.randint(4, 20)
        
# #         dataset.append({
# #             "table_id": table_id,
# #             "processes": generate_processes(table_type, num_processes),
# #             "time_quantum": generate_time_quantum(table_type)
# #         })
    
# #     return dataset

# # def save_to_csv(dataset: List[Dict], filename: str):
# #     with open(filename, 'w', newline='') as csvfile:
# #         writer = csv.writer(csvfile)
# #         writer.writerow(['table_id', 'time_quantum', 'processes'])
        
# #         for table in dataset:
# #             processes_str = ';'.join([f"{p[0]},{p[1]},{p[2]}" for p in table['processes']])
# #             writer.writerow([
# #                 table['table_id'],
# #                 table['time_quantum'] if table['time_quantum'] is not None else '',
# #                 processes_str
# #             ])

# # def save_to_json(dataset: List[Dict], filename: str):
# #     with open(filename, 'w') as jsonfile:
# #         json.dump(dataset, jsonfile, indent=2)

# # # Generate & save
# # dataset = generate_dataset()
# # # save_to_csv(dataset, 'cpu_scheduling_tables.csv')
# # save_to_json(dataset, 'cpu_scheduling_tables.json')
# # import random
# # import json
# # from typing import List, Dict

# # def generate_processes(table_type: str, num_processes: int) -> List[List[float]]:
# #     if table_type == 'A':  # SJF (short jobs)
# #         bursts = [1, 1, 2, 2, 3, 5]
# #         return [
# #             [round(random.uniform(0, 10), 1), random.choice(bursts), random.randint(1, 10)]
# #             for _ in range(num_processes)
# #         ]
    
# #     elif table_type == 'B':  # Round Robin (mixed bursts and clustered arrivals)
# #         cluster_time = round(random.uniform(0, 5), 1)
# #         bursts = [2, 3, 5, 8, 10]
# #         return [
# #             [round(max(0, cluster_time + random.uniform(-1, 1)), 1), random.choice(bursts), random.randint(3, 7)]
# #             for _ in range(num_processes)
# #         ]
    
# #     elif table_type == 'C':  # Priority (1 very high priority)
# #         high_prio_idx = random.randint(0, num_processes - 1)
# #         return [
# #             [round(random.uniform(0, 15), 1), random.randint(1, 10), 1 if i == high_prio_idx else random.randint(5, 10)]
# #             for i in range(num_processes)
# #         ]
    
# #     elif table_type == 'D':  # FCFS (all arrive at t=0, long bursts)
# #         base_burst = random.randint(8, 20)
# #         return [
# #             [0.0, base_burst + random.randint(-2, 2), random.randint(1, 10)]
# #             for _ in range(num_processes)
# #         ]

# # def generate_time_quantum() -> int:
# #     return random.randint(2, 5)

# # def generate_dataset(num_tables: int = 1000) -> List[Dict]:
# #     dataset = []
# #     table_types = ['A'] * (num_tables // 4) + ['B'] * (num_tables // 4) + \
# #                   ['C'] * (num_tables // 4) + ['D'] * (num_tables // 4)
# #     random.shuffle(table_types)

# #     for table_id, table_type in enumerate(table_types, 1):
# #         num_processes = random.randint(5, 10)
# #         dataset.append({
# #             "table_id": table_id,
# #             "processes": generate_processes(table_type, num_processes),
# #             "time_quantum": generate_time_quantum(),
# #             "ideal_algo": table_type  # optional ML label
# #         })

# #     return dataset

# # # Save to JSON
# # dataset = generate_dataset()
# # with open("cpu_scheduling_tables.json", "w") as f:
# #     json.dump(dataset, f, indent=2)
# import random
# import json
# from typing import List, Dict

# def generate_random_processes(num_processes: int) -> List[List[int]]:
#     return [
#         [
#             int(random.uniform(0, 20)),      # arrival_time
#             random.randint(1, 20),                # burst_time
#             random.randint(1, 10)                 # priority
#         ]
#         for _ in range(num_processes)
#     ]

# def generate_non_sjf_friendly_processes(num_processes: int) -> List[List[int]]:
#     processes = []

#     # Add one long, important job at the beginning
#     processes.append([0, random.randint(15, 25), 1])  # High priority, long job

#     # Add many small, low-priority jobs that arrive later
#     for _ in range(num_processes - 1):
#         arrival_time = random.randint(2, 15)
#         burst_time = random.randint(1, 5)
#         priority = random.randint(5, 10)
#         processes.append([arrival_time, burst_time, priority])

#     return processes
# def generate_challenging_dataset(num_processes):
#         processes = []

#         for i in range(num_processes):
#             arrival = 0 if i < num_processes - 3 else random.randint(10, 30)
#             burst = random.choice([1, 2]) if i < num_processes - 3 else random.randint(10, 20)
#             priority = random.randint(1, 10)
#             processes.append([arrival, burst, priority])
#         return processes
        



# def generate_time_quantum() -> int:
#     return random.randint(2, 10)

# def generate_dataset(num_tables: int = 20000) -> List[Dict]:
#     dataset = []

#     # for table_id in range(1, num_tables + 1):
#     #     num_processes = random.randint(10, 20)
#     #     dataset.append({
#     #         "table_id": table_id,
#     #         "processes": generate_random_processes(num_processes),
#     #         "time_quantum": generate_time_quantum()
#     #     })

#     # for table_id in range(1, num_tables + 1):
#     #     num_processes = random.randint(10, 20)
#     #     dataset.append({
#     #         "table_id": table_id,
#     #         "processes": generate_non_sjf_friendly_processes(num_processes),
#     #         "time_quantum": generate_time_quantum()
#     #     })
#     for table_id in range(1, num_tables + 1):
#         num_processes = random.randint(10, 20)
#         dataset.append({
#             "table_id": table_id,
#             "processes": generate_challenging_dataset(num_processes),
#             "time_quantum": generate_time_quantum()
#         })
    

#     return dataset

# # Save to JSON
# dataset = generate_dataset()
# with open("cpu_scheduling_random_tables.json", "w") as f:
#     json.dump(dataset, f, indent=2)
import random
import json

def generate_balanced_dataset(num_tables: int = 1000, output_file="cpu_scheduling_balanced.json"):
    dataset = []
    types = ['FCFS', 'SJF', 'RR', 'Priority'] * (num_tables // 4)
    random.shuffle(types)

    for table_id, table_type in enumerate(types, 1):
        num_processes = random.randint(10, 20)
        processes = []
        
        if table_type == 'FCFS':
            for _ in range(num_processes):
                processes.append([
                    0,  # arrivalTime
                    random.randint(3, 15),  # burstTime
                    random.randint(1, 10)  # priority
                ])

        elif table_type == 'SJF':
            for _ in range(num_processes):
                arrival = round(random.uniform(0, 10))
                burst = random.choice([1, 2, 3, 5, 8])
                priority = random.randint(1, 10)
                processes.append([arrival, burst, priority])

        elif table_type == 'RR':
            cluster_time = random.randint(0, 5)
            for _ in range(num_processes):
                arrival = round(cluster_time + random.uniform(-2, 2))
                burst = random.randint(3, 8)
                priority = random.randint(1, 10)
                processes.append([max(0, arrival), burst, priority])

        elif table_type == 'Priority':
            high_prio_idx = random.sample(range(num_processes), k=2)
            for i in range(num_processes):
                arrival = random.randint(0, 15)
                burst = random.randint(2, 10)
                priority = 1 if i in high_prio_idx else random.randint(5, 10)
                processes.append([arrival, burst, priority])

        dataset.append({
            "table_id": table_id,
            "processes": processes,
            "time_quantum": random.randint(2, 10)
        })

    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"✅ Balanced dataset saved to {output_file}")

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "cpu_scheduling_balanced.json")

def generate_aggressively_balanced_dataset(num_tables: int = 20000, output_file=file_path):
    dataset = []
    modes = ['FCFS', 'SJF_Breaker', 'RR_Fair', 'Priority_Bias'] * (num_tables // 4)
    random.shuffle(modes)

    for table_id, mode in enumerate(modes, 1):
        num_processes = random.randint(10, 20)
        processes = []

        if mode == 'FCFS':
            # All processes arrive at time 0, longer burst times
            for _ in range(num_processes):
                processes.append([
                    0,  # arrivalTime
                    random.randint(6, 15),  # burstTime
                    random.randint(1, 10)  # priority
                ])

        elif mode == 'SJF_Breaker':
            # Early long burst job, followed by short ones
            processes.append([
                0,  # early long burst
                random.randint(15, 25),
                random.randint(5, 10)
            ])
            for _ in range(num_processes - 1):
                arrival = random.randint(3, 15)
                burst = random.randint(1, 5)
                priority = random.randint(1, 10)
                processes.append([arrival, burst, priority])
            random.shuffle(processes)

        elif mode == 'RR_Fair':
            # All same burst time but varied arrival
            burst = random.randint(4, 6)
            for _ in range(num_processes):
                arrival = random.randint(0, 10)
                processes.append([arrival, burst, random.randint(1, 10)])

        elif mode == 'Priority_Bias':
            # Late high-priority processes and early low-priority hogs
            for _ in range(num_processes):
                arrival = random.randint(0, 15)
                burst = random.randint(2, 10)
                # Inject few high-priority latecomers
                if random.random() < 0.15:
                    arrival = random.randint(10, 15)
                    priority = 1
                else:
                    priority = random.randint(5, 10)
                processes.append([arrival, burst, priority])
            random.shuffle(processes)

        dataset.append({
            "table_id": table_id,
            "processes": processes,
            "time_quantum": random.randint(2, 5)
        })
    
    dataset += (generate_fcfs_favored_tables(num_tables+1, 10000))

    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"✅ Aggressively balanced dataset saved to {output_file}")



def generate_fcfs_favored_tables(next_table_id: int, count: int):
    time_quantum = 4
    new_entries = []
    generated = 0

    while generated < count:
        num_processes = random.randint(6, 10)
        processes = []

        # One long early job to favor FCFS
        first_arrival = 0
        first_burst = random.randint(20, 30)  # Very long burst
        first_priority = random.randint(4, 6)  # Neutral priority
        processes.append([first_arrival, first_burst, first_priority])

        # Rest: small bursts, late arrivals
        for _ in range(1, num_processes):
            arrival = random.randint(8, 20)  # Late arrivals
            burst = random.randint(2, 5)     # Shorter bursts
            priority = random.randint(3, 7)  # Balanced priority
            processes.append([arrival, burst, priority])

        # Inject a mild variation every few tables
        if random.random() < 0.2:
            # One mid-priority process shows up early with small burst
            processes.append([random.randint(1, 3), random.randint(2, 4), random.randint(5, 7)])

        new_entries.append({
            "table_id": next_table_id,
            "processes": processes,
            "time_quantum": time_quantum
        })

        generated += 1
        next_table_id += 1

    return new_entries

# Example usage
# generate_balanced_dataset(20000)
generate_aggressively_balanced_dataset(50000)


