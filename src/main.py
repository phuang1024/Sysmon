import argparse
import os
import time
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
pygame.init()


def refresh(graphs):
    pass


def redraw(surface):
    print("redraw")


def main(args):
    # Create graph objects.
    graphs = []
    # TODO

    surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("System Monitor")

    last_refresh = 0
    while True:
        time.sleep(1 / 60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.VIDEORESIZE:
                redraw(surface)

        if time.time() - last_refresh > args.rate:
            last_refresh = time.time()
            refresh(graphs)
            redraw(surface)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--cpu", action="store_true")
    parser.add_argument("--no-cpu", dest="cpu", action="store_false")
    parser.add_argument("--memory", action="store_true")
    parser.add_argument("--no-memory", dest="memory", action="store_false")
    parser.set_defaults(cpu=True, memory=True)

    parser.add_argument("-r", "--rate", type=float, default=0.2, help="Refresh rate.")
    parser.add_argument("-t", "--time", type=float, default=60, help="Graph X axis length.")

    args = parser.parse_args()

    main(args)
