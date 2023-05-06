import time

import cv2
import numpy as np
import pygame

from utils import random_color


class Graph:
    """
    Extend from this.
    """

    name = "Graph"
    n_lines = 0
    supports_avg = True

    def __init__(self, length, refresh_rate: float):
        # Set this from outside.
        self.average = False
        self.length = length
        self.refresh_rate = refresh_rate
        self.last_update = time.time()
        self.data = np.zeros((self.n_lines, length), dtype=float)

    def update(self):
        """
        Call refresh and roll over data.
        """
        data, labels = self.refresh()

        self.data = np.roll(self.data, -1, axis=1)
        self.data[:, -1] = data

        self.labels = labels

        self.last_update = time.time()

    def draw_graph(self, width, height, args):
        image = np.zeros((height, width, 3), dtype=np.uint8)

        do_avg = self.average and self.supports_avg
        for i, line in enumerate(self.data):
            color = random_color(i)
            # Dim individual if average is set.
            if do_avg:
                color = color * 0.3
            self.draw_line(image, line, color)
        if do_avg:
            data = np.mean(self.data, axis=0)
            self.draw_line(image, data, random_color(0))

        # Convert to pygame surface
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "RGB")

        return image

    def draw_line(self, image, data, color):
        if len(data) <= 1:
            dx = 0
        else:
            dx = image.shape[1] / (len(data) - 1)

        # Previous (x, y) point on image.
        prev = None
        # X offset for smooth scrolling.
        offset_x = -1 * (time.time()-self.last_update) / self.refresh_rate * dx
        offset_x = int(offset_x)
        for i, value in enumerate(data):
            point = (
                int(i*dx) + offset_x,
                int(np.interp(value, (0, 1), (image.shape[0]-1, 0))),
            )

            # Draw connecting line.
            if prev is not None:
                cv2.line(image, prev, point, color * 0.6, 1, cv2.LINE_AA)
            prev = point

            # Draw point.
            cv2.circle(image, point, 1, color, -1, cv2.LINE_AA)

    def draw_labels(self, width, height, args, font):
        image = pygame.Surface((width, height))

        labels = [self.name, "", *self.labels]
        for i, label in enumerate(labels):
            y = (args.font_size+2) * i
            text = font.render(label, True, (255, 255, 255))
            image.blit(text, (0, y))

        return image

    def refresh(self) -> tuple[list[float], list[str]]:
        """
        Implement this in the subclass. Return a sequence of values for each graph.
        Min-max should be 0-1

        :return: (values, labels)
        """
        return ([], [])
