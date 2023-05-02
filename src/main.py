import argparse
import os
import time
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
pygame.init()

from cpu import Cpu

ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FONT = os.path.join(ROOT, "assets", "ubuntu-condensed.ttf")
# Set in `if __name__ == "__main__"`
FONT = None


def refresh(graphs):
    for graph in graphs:
        graph.update()


def redraw(surface, graphs, args):
    surface.fill((0, 0, 0))

    # Compute height
    total_graph_factors = len(graphs) + (len(graphs)+1) * args.margin
    graph_height = surface.get_height() / total_graph_factors
    margin = graph_height * args.margin

    # Compute width
    total_width = surface.get_width() - 2*margin
    avail_width = total_width - margin
    graph_width = avail_width / (1 + args.labels)
    label_width = graph_width * args.labels
    label_x = 2*margin + graph_width

    y = margin
    for graph in graphs:
        # Graph
        img = graph.draw_graph(int(graph_width), int(graph_height), args)
        surface.blit(img, (margin, y))
        pygame.draw.rect(surface, (255, 255, 255), (margin, y, graph_width, graph_height), 1)

        # Labels
        labels = graph.draw_labels(int(label_width), int(graph_height), args, FONT)
        surface.blit(labels, (label_x, y))

        y += graph_height + margin


def main(args):
    length = int(args.time / args.rate)

    # Create graph objects.
    graphs = []
    if args.cpu:
        graphs.append(Cpu(length))

    surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("System Monitor")

    last_refresh = 0
    while True:
        time.sleep(1 / 60)
        pygame.display.update()

        need_redraw = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.VIDEORESIZE:
                need_redraw = True

            elif event.type == pygame.KEYDOWN:
                need_redraw = True
                if event.key == pygame.K_a:
                    for graph in graphs:
                        graph.average = not graph.average

        if time.time() - last_refresh > args.rate:
            last_refresh = time.time()
            refresh(graphs)
            need_redraw = True

        if need_redraw:
            redraw(surface, graphs, args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--cpu", action="store_true")
    parser.add_argument("--no-cpu", dest="cpu", action="store_false")
    parser.add_argument("--memory", action="store_true")
    parser.add_argument("--no-memory", dest="memory", action="store_false")
    parser.set_defaults(cpu=True, memory=True)

    parser.add_argument("-r", "--rate", type=float, default=0.4, help="Refresh rate.")
    parser.add_argument("-t", "--time", type=float, default=60, help="Graph X axis length.")
    parser.add_argument("--font", type=str, default=DEFAULT_FONT, help="Font to use for labels.")
    parser.add_argument("--margin", type=float, default=0.2, help="Spacing between graphs as factor of graph height.")
    parser.add_argument("--labels", type=float, default=0.3, help="Space for labels as factor of graph width.")

    args = parser.parse_args()

    FONT = pygame.font.Font(args.font, 16)

    main(args)
