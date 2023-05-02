import numpy as np
import psutil

from graph import Graph


class Cpu(Graph):
    n_lines = psutil.cpu_count()

    def refresh(self):
        data = np.array(psutil.cpu_percent(percpu=True))
        data = data / 100
        return data
