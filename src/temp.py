import numpy as np
import psutil

from graph import Graph


class Temperature(Graph):
    name = "Temperature"
    n_lines = len([e for e in psutil.sensors_temperatures()["coretemp"] if e.label.startswith("Core")])
    supports_avg = True

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
