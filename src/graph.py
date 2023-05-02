import cv2
import numpy as np
import pygame


class Graph:
    """
    Extend from this.
    """

    n_lines = 0

    def __init__(self, length):
        # Set this from outside.
        self.average = False
        self.length = length
        self.data = np.zeros((self.n_lines, length), dtype=float)

    def update(self):
        """
        Call refresh and roll over data.
        """
        self.data = np.roll(self.data, -1, axis=1)
        self.data[:, -1] = self.refresh()

    def draw(self, width, height, args):
        image = np.zeros((height, width, 3), dtype=np.uint8)

        if self.average:
            data = np.mean(self.data, axis=0)
            self.draw_line(image, data, (255, 255, 255))
        else:
            for line in self.data:
                self.draw_line(image, line, (255, 255, 255))

    def draw_line(self, image, data, color):
        if len(data) <= 1:
            dx = 0
        else:
            dx = image.shape[1] / (len(data) - 1)

        # Previous (x, y) point on image.
        prev = None
        for i, value in enumerate(data):
            point = (
                int(i*dx),
                np.interp(value, (0, 1), (image.shape[0]-1, 0))
            )

            # Draw connecting line.
            if prev is not None:
                cv2.line(image, prev, point, color, 1, cv2.LINE_AA)

            # Draw point.
            cv2.circle(image, point, 2, color, -1, cv2.LINE_AA)

    def refresh(self) -> list[float]:
        """
        Implement this in the subclass. Return a sequence of values for each graph.
        Min-max should be 0-1
        """
        return []
