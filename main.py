import matplotlib.pyplot as plt
import re


def load_data(filepath):
    runs = {}
    with open(filepath, 'r') as file:
        for line in file:
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


def plot_speedup(runs, graph_title):
    plt.figure(figsize=(10, 6))
    for run, durations in runs.items():
        base_duration = durations[1]
        x = sorted(durations.keys())
        y = [base_duration / durations[cpu] for cpu in x]
        plt.plot(x, y, marker='o', label=f'Run {run}')

    plt.title(graph_title)
    plt.xlabel('Number of CPU Cores')
    plt.ylabel('Speedup (Single-core duration / Multi-core duration)')
    plt.grid(True)
    plt.legend()
    plt.xticks(range(0, 65, 4))
    plt.tight_layout()
    # plt.show()

    filename = title_to_snake_case(graph_title) + '.png'
    plt.savefig(filename)
    print(f"Plot saved as: {filename}")


if __name__ == "__main__":
    filepath = 'harmonic_data.txt'
    graph_title = "Harmonic Progression Sum"
    run_data = load_data(filepath)
    plot_speedup(run_data, graph_title)
