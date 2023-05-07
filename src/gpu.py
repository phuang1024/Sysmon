import re
from subprocess import check_output

import numpy as np
import psutil

from graph import Graph


def read_nvidia():
    info = check_output(["nvidia-smi"]).decode()

    temp = int(re.findall(r"(\d+)C", info)[0])
    power = int(re.findall(r"(\d+)W", info)[0])
    mem_used = int(re.findall(r"(\d+)MiB", info)[0])
    mem_total = int(re.findall(r"(\d+)MiB", info)[1])
    util = int(re.findall(r"(\d+)%", info)[1])

    return {
        "temp": temp,
        "power": power,
        "mem_used": mem_used,
        "mem_total": mem_total,
        "util": util,
    }


class GpuUtil(Graph):
    name = "GPU Utilization"
    n_lines = 0

    def init(self):
        try:
            read_nvidia()
            self.n_lines = 1
        except Exception:
            pass

    def refresh(self):
        state = read_nvidia()
        labels = [f"Utilization: {state['util']}%"]
        data = [state["util"] / 100]
        return data, labels


class GpuTemp(Graph):
    name = "GPU Temperature"
    n_lines = 0

    def init(self):
        try:
            read_nvidia()
            self.n_lines = 1
        except Exception:
            pass

    def refresh(self):
        state = read_nvidia()
        labels = [f"Temperature: {state['temp']} C"]
        data = [state["temp"] / 100]
        return data, labels


class GpuMem(Graph):
    name = "GPU Memory"
    n_lines = 0

    def init(self):
        try:
            read_nvidia()
            self.n_lines = 1
        except Exception:
            pass

    def refresh(self):
        state = read_nvidia()
        labels = [
            f"Used: {state['mem_used']} MiB",
            f"Total: {state['mem_total']} MiB",
        ]
        data = [state["mem_used"] / state["mem_total"]]
        return data, labels
