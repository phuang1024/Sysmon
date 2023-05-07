import numpy as np
import psutil

from graph import Graph


class Memory(Graph):
    name = "Memory"
    n_lines = 1

    def refresh(self):
        memory = psutil.virtual_memory()
        data = [memory.percent / 100]
        labels = (
            f"Total {memory.total / 1024 ** 3:.2f} GB",
            f"Used: {memory.used / 1024 ** 3:.2f} GB, {int(memory.percent)}%",
            f"Free: {memory.available / 1024 ** 3:.2f} GB",
        )

        return data, labels


class Cached(Graph):
    name = "Cached"
    n_lines = 1

    def refresh(self):
        memory = psutil.virtual_memory()
        data = [memory.cached / memory.total]
        labels = (
            f"Cached: {memory.cached / 1024 ** 3:.2f} GB, {int(memory.cached / memory.total * 100)}%",
        )

        return data, labels


class Swap(Graph):
    name = "Swap"
    n_lines = 1

    def refresh(self):
        memory = psutil.swap_memory()
        data = [memory.percent / 100]
        labels = (
            f"Total {memory.total / 1024 ** 3:.2f} GB",
            f"Used: {memory.used / 1024 ** 3:.2f} GB, {int(memory.percent)}%",
            f"Free: {memory.free / 1024 ** 3:.2f} GB",
        )

        return data, labels
