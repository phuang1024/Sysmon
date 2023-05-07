import numpy as np
import psutil

from graph import Graph


class CpuUtil(Graph):
    name = "CPU Utilization"
    n_lines = psutil.cpu_count()

    def refresh(self):
        data = np.array(psutil.cpu_percent(percpu=True))
        data = data / 100

        labels = (
            f"Cores: {len(data)}",
            f"N > 50%: {np.sum(data > 0.5)}",
            f"Average: {int(100*np.average(data))}%",
            f"Max: {int(100*np.max(data))}%",
        )

        return data, labels


class CpuTemp(Graph):
    name = "CPU Temperature"
    n_lines = 0
    supports_avg = True

    def init(self):
        temp = psutil.sensors_temperatures()
        if "coretemp" in temp:
            self.n_lines = len([e for e in temp["coretemp"] if e.label.startswith("Core")])

    def refresh(self):
        temp = psutil.sensors_temperatures()
        data = []
        for entry in temp["coretemp"]:
            if entry.label.startswith("Core"):
                data.append(entry.current)
        data = np.array(data)

        labels = (
            f"Average: {np.mean(data):.1f} C",
            f"Max: {np.max(data):.1f} C",
        )

        data /= 100
        return data, labels
