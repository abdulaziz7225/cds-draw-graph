import os
import matplotlib.pyplot as plt
import re


def load_data(filepath):
    runs = {}
    with open(filepath, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            _, run, cpus, duration = line.strip().split(';')
            run = int(run.strip())
            cpus = int(cpus.strip())
            duration = int(duration.strip())

            if run not in runs:
                runs[run] = {}
            runs[run][cpus] = duration
    return runs


def title_to_snake_case(title):
    title = title.strip().lower()
    title = re.sub(r'[^a-z0-9]+', '_', title)
    return title.strip('_')


def plot_speedup(all_run_data, graph_title):
    plt.figure(figsize=(12, 7))
    
    for running_times in all_run_data.values():
        for run, durations in running_times.items():
            base_duration = durations.get(1)
            if not base_duration:
                continue
            x = sorted(durations.keys())
            y = [base_duration / durations[cpu] for cpu in x]
            plt.plot(x, y, marker='o', label=f"Run {run}")

    plt.title(graph_title)
    plt.xlabel('Number of CPU Cores')
    plt.ylabel('Speedup (Single-core duration / Multi-core duration)')
    plt.grid(True)
    plt.legend()
    plt.xticks(range(0, 65, 4))
    plt.tight_layout()

    # Ensure 'out' folder exists
    os.makedirs('out', exist_ok=True)

    filename = os.path.join('out', title_to_snake_case(graph_title) + '.png')
    plt.savefig(filename)
    print(f"\n✅ Plot saved as: {filename}")


if __name__ == "__main__":
    folder_name = input("Enter the folder name containing the .txt files: ").strip()
    graph_title = input("Enter the graph title: ").strip()

    if not os.path.isdir(folder_name):
        print(f"❌ Folder '{folder_name}' not found.")
        exit(1)

    all_run_data = {}
    for filename in sorted(os.listdir(folder_name)):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_name, filename)
            run_data = load_data(filepath)
            all_run_data[filename] = run_data

    if not all_run_data:
        print("❌ No .txt files found in the folder.")
    else:
        plot_speedup(all_run_data, graph_title)
