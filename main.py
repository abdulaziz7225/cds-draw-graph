import os
import matplotlib.pyplot as plt
import re
import csv


def load_data(filepath):
    runs = dict()
    with open(filepath, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)
        if header[0].strip().lower() != 'program':
            # Not a header, reset file pointer
            file.seek(0)
            reader = csv.reader(file, delimiter=';')

        for row in reader:
            if len(row) != 4:
                continue
            try:
                run = int(row[1])
                cpus = int(row[2])
                duration = int(row[3])
            except ValueError:
                continue

            if run not in runs:
                runs[run] = []
            runs[run].append((cpus, duration))

    return runs


def title_to_snake_case(title):
    title = title.strip().lower()
    title = re.sub(r'[^a-z0-9]+', '_', title)
    return title.strip('_')


def plot_speedup(all_run_data, graph_title):
    plt.figure(figsize=(12, 7))

    for run in all_run_data:
        base_duration = all_run_data[run][0][1]
        if not base_duration:
            continue
        x = [cpu for cpu, _ in all_run_data[run]]
        y = [base_duration / duration for _, duration in all_run_data[run]]
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


def main():
    file_name = input("Enter the filename: ").strip()
    graph_title = input("Enter the graph title: ").strip()

    if not file_name:
        print("File path cannot be empty.")
        return

    input_path = os.path.join('input', file_name)
    if not os.path.isfile(input_path):
        print(f"❌ File '{file_name}' not found in the 'input' folder.")
        return

    all_run_data = load_data(input_path)
    if not all_run_data:
        print("❌ No .txt files found in the folder.")
    else:
        plot_speedup(all_run_data, graph_title)


if __name__ == "__main__":
    main()
