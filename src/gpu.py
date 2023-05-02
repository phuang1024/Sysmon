import re
from subprocess import check_output

import numpy as np
import psutil

from graph import Graph


class Gpu(Graph):
    name = "GPU"
    n_lines = 4
    supports_avg = False

    def refresh(self):
        info = check_output(["nvidia-smi"]).decode()

        temp = int(re.findall(r"(\d+)C", info)[0])
        power = int(re.findall(r"(\d+)W", info)[0])
        mem_used = int(re.findall(r"(\d+)MiB", info)[0])
        mem_total = int(re.findall(r"(\d+)MiB", info)[1])
        util = int(re.findall(r"(\d+)%", info)[1])

        labels = (
            f"Temperature: {temp}C",
            f"Power: {power}W",
            f"Memory: {mem_used}MiB / {mem_total}MiB ({mem_used / mem_total * 100:.1f}%)",
            f"Utilization: {util}%",
        )

        data = np.array([
            temp / 100,
            power / 1000,
            mem_used / mem_total,
            util / 100,
        ])

        return data, labels
