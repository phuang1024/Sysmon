import numpy as np
import psutil

from graph import Graph


class Memory(Graph):
    name = "Memory"
    n_lines = 2
    supports_avg = False

    def refresh(self):
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        data = np.array([memory.percent, swap.percent]) / 100

        labels = (
            f"Memory: Total {memory.total / 1024 ** 3:.2f} GB",
            f"Used: {memory.used / 1024 ** 3:.2f} GB, {int(memory.percent)}%",
            f"Cached: {memory.cached / 1024 ** 3:.2f} GB",
            f"Free: {memory.available / 1024 ** 3:.2f} GB",
            "",
            f"Swap: Total {swap.total / 1024 ** 3:.2f} GB",
            f"Used: {swap.used / 1024 ** 3:.2f} GB, {int(swap.percent)}%",
            f"Free: {swap.free / 1024 ** 3:.2f} GB",
        )

        return data, labels
