import logging
from dataclasses import dataclass
from dataclasses import field
from queue import PriorityQueue
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from .grid import Grid
from .hex import Hex
from .hex_math import HexMath


LOGGER = logging.getLogger(__file__)


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


PATH_LIMIT = 100


def find_path(grid: Grid, start: Hex, goal: Hex) -> Dict[Hex, Optional[Hex]]:
    frontier = PriorityQueue()  # type: ignore
    frontier.put(PrioritizedItem(item=start, priority=0))
    came_from: Dict[Hex, Optional[Hex]] = dict()
    cost_so_far: Dict[Hex, int] = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    # If goal is blocked, there is no path
    if goal.is_blocked:
        return came_from

    while not frontier.empty():
        current = frontier.get()
        if isinstance(current, PrioritizedItem):
            current = current.item

        if current == goal:
            break

        for next in grid.neighbours(current):
            if next.is_blocked:
                continue
            new_cost = cost_so_far[current] + next.cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + HexMath.distance(goal, next)
                frontier.put(PrioritizedItem(item=next, priority=int(priority)))
                came_from[next] = current

    return came_from


def get_path(start: Hex, end: Hex, came_from: Dict[Hex, Optional[Hex]]) -> List[Hex]:
    path = [end]
    hex = end
    count = 0
    while hex != start:
        count += 1
        hex = came_from.get(hex, None)  # type: ignore
        if hex is None:
            return []
        path.insert(0, hex)

    return path
