import logging
from dataclasses import dataclass
from dataclasses import field
from queue import PriorityQueue
from typing import Any
from typing import Dict
from typing import Optional

from .grid import Grid
from .hex import Hex


LOGGER = logging.getLogger(__file__)


def heuristic(a: Hex, b: Hex) -> int:
    # Manhattan distance on a square grid
    return int(abs(a.q - b.q) + abs(a.r - b.r))


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


PATH_LIMIT = 100


def pathfinding(grid: Grid, start: Hex, goal: Hex) -> Dict[Hex, Optional[Hex]]:
    frontier = PriorityQueue()  # type: ignore
    frontier.put(PrioritizedItem(item=start, priority=0))
    came_from: Dict[Hex, Optional[Hex]] = dict()
    cost_so_far: Dict[Hex, int] = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if isinstance(current, PrioritizedItem):
            current = current.item

        if current == goal:
            break

        for next in grid.neighbours(current):
            new_cost = cost_so_far[current] + next.cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(PrioritizedItem(item=next, priority=priority))
                came_from[next] = current

    return came_from
