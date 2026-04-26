from maze.maze import Maze
from maze.side import Side


def get_shortest_path(maze: Maze) -> list[Side]:
    queue: list[tuple[int, int]] = []
    visited: set[tuple[int, int]] = set()
    parent_map: dict[tuple[int, int], tuple[tuple[int, int], Side]] = {}
    path: list[Side] = []
    found: bool = False

    queue.append(maze.entry)
    visited.add(maze.entry)

    while queue:
        current = queue.pop(0)
        cx, cy = current

        if current == maze.exit:
            found = True
            break

        for side, ax, ay in maze.get_reachable_adjacent_cells(cx, cy):
            adjacent_cell_coords = (ax, ay)
            if adjacent_cell_coords not in visited:
                visited.add(adjacent_cell_coords)
                parent_map[adjacent_cell_coords] = current, side
                queue.append(adjacent_cell_coords)

    if not found:
        raise ValueError(
            "No path found between "
            f"entry {maze.entry} and exit {maze.exit}."
        )

    current = maze.exit
    while current != maze.entry:
        parent, direction = parent_map[current]
        path.append(direction)
        current = parent

    path.reverse()

    return path


def get_path_string(path: list[Side]) -> str:
    return "".join(direction.to_char() for direction in path)


def get_path_coords(maze: Maze, path: list[Side]) -> list[tuple[int, int]]:
    current = maze.entry
    path_coords: list[tuple[int, int]] = []
    path_coords.append(current)

    for side in path:
        dx, dy = side.delta()
        x, y = current

        current = (x + dx, y + dy)
        path_coords.append(current)

    return path_coords
