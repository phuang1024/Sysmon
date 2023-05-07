import argparse
import os
import time
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
pygame.init()

from cpu import *
from gpu import *
from memory import *

ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FONT = os.path.join(ROOT, "assets", "ubuntu-condensed.ttf")
# Set in `if __name__ == "__main__"`
FONT = None


def foreach_graph(graphs):
    for _, g in graphs:
        for graph in g:
            yield graph


def refresh(graphs):
    for graph in foreach_graph(graphs):
        graph.update()


def redraw(surface, graphs, tab, args):
    surface.fill((0, 0, 0))

    # Compute height
    total_graph_factors = len(graphs) + (len(graphs)+1) * args.margin
    graph_height = (surface.get_height()-20) / total_graph_factors
    margin = graph_height * args.margin

    # Compute width
    total_width = surface.get_width() - 2*margin
    avail_width = total_width - margin
    graph_width = avail_width / (1 + args.labels)
    label_width = graph_width * args.labels
    label_x = 2*margin + graph_width

    y = margin
    for graph in graphs[tab][1]:
        # Graph
        img = graph.draw_graph(int(graph_width), int(graph_height), args)
        surface.blit(img, (margin, y))
        pygame.draw.rect(surface, (255, 255, 255), (margin, y, graph_width, graph_height), 1)

        # Labels
        labels = graph.draw_labels(int(label_width), int(graph_height), args, FONT)
        surface.blit(labels, (label_x, y))

        y += graph_height + margin

    # Draw tabs
    tab_width = surface.get_width() / len(graphs)
    tab_width = int(min(tab_width, 100))
    for i in range(len(graphs)):
        x = i * tab_width
        color = (215, 215, 255) if i == tab else (190, 190, 190)
        pygame.draw.rect(surface, color, (x, 0, tab_width, 20), 0, 3)
        pygame.draw.rect(surface, (255, 255, 255), (x, 0, tab_width, 20), 1, 3)

        text = FONT.render(graphs[i][0], True, (0, 0, 0))
        text_x = x + (tab_width - text.get_width()) / 2
        text_y = (20 - text.get_height()) / 2
        surface.blit(text, (text_x, text_y))


def main(args):
    length = int(args.time / args.rate)

    graphs = (
        ("CPU", (
            CpuUtil(length, args.rate),
            CpuTemp(length, args.rate),
        )),
        ("Memory", (
            Memory(length, args.rate),
            Cached(length, args.rate),
            Swap(length, args.rate),
        )),
        ("GPU", (
            GpuUtil(length, args.rate),
            GpuTemp(length, args.rate),
        )),
    )

    surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("System Monitor")

    tab = 0
    last_refresh = 0
    while True:
        time.sleep(1 / 40)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    for graph in foreach_graph(graphs):
                        graph.average = not graph.average

                elif pygame.K_1 <= event.key <= pygame.K_9:
                    tab = event.key - pygame.K_1
                    tab = min(tab, len(graphs)-1)

        if time.time() - last_refresh > args.rate:
            last_refresh = time.time()
            refresh(graphs)

        redraw(surface, graphs, tab, args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rate", type=float, default=0.4, help="Refresh rate.")
    parser.add_argument("-t", "--time", type=float, default=60, help="Graph X axis length.")
    parser.add_argument("--font", type=str, default=DEFAULT_FONT, help="Font to use for labels.")
    parser.add_argument("--font-size", type=int, default=17, help="Font size to use for labels.")
    parser.add_argument("--margin", type=float, default=0.2, help="Spacing between graphs as factor of graph height.")
    parser.add_argument("--labels", type=float, default=0.2, help="Space for labels as factor of graph width.")
    parser.add_argument("--scroll", action="store_true", help="Smooth scrolling in time dimension.")

    args = parser.parse_args()

    FONT = pygame.font.Font(args.font, args.font_size)

    main(args)
