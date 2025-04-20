rname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "processes.json")
with open(file_path) as f:
    data = json.load(f)