import numpy as np
import psutil

from graph import Graph


class Cpu(Graph):
    name = "CPU"
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
