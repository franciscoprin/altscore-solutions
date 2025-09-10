import re
from collections import deque

# Additional stop in the way of ^ to #, notice that these aditional stops are the radar reads.
ENEMY_SHIP_STOP_SYMBOL = "p"


class Node:
    def __init__(self, value: str, childrens: list['Node'], x: str | None = None, y: int | None = None):
        self.value = value
        self.childrens = childrens
        # Grid coordinates (column x=j, row y=i) will be set when building the grid
        self.x: str | None = x
        self.y: int | None = y

    def __repr__(self) -> str:
        return f"{self.value}(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return self.__repr__()


def in_bounds(i: int, j: int, rows: int, cols: int) -> bool:
    return 0 <= i < rows and 0 <= j < cols

# ANSI color helpers for pretty printing
ANSI = {
    "reset": "\033[0m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
}

def colorize(ch: str, enable: bool) -> str:
    if not enable:
        return ch
    # Map symbols to colors
    if ch == ENEMY_SHIP_STOP_SYMBOL:  # stop marker
        return f"{ANSI['red']}{ch}{ANSI['reset']}"
    if ch == '^':  # origin
        return f"{ANSI['cyan']}{ch}{ANSI['reset']}"
    if ch == '#':  # destination
        return f"{ANSI['green']}{ch}{ANSI['reset']}"
    if ch == '$':  # obstacle
        return f"{ANSI['yellow']}{ch}{ANSI['reset']}"
    if ch == '*':  # path overlay
        return f"{ANSI['magenta']}{ch}{ANSI['reset']}"
    if ch == '0':  # empty
        return f"{ANSI['dim']}{ch}{ANSI['reset']}"
    return ch


class MovementModel:
    """Learns direction preferences from observed enemy moves.

    Directions are deltas in (di, dj) with values in {-1, 0, 1} excluding (0,0).
    Higher bias means higher preference when breaking ties among shortest paths.
    """

    def __init__(self):
        # Initialize bias with a deterministic default order similar to current code
        # Default: Down, Up, Left, Right, then diagonals DR, DL, UR, UL
        self.bias: dict[tuple[int, int], float] = {
            (1, 0): 4.0,   # Down
            (-1, 0): 3.0,  # Up
            (0, -1): 2.0,  # Left
            (0, 1): 1.0,   # Right
            (1, 1): 0.4,   # Down-Right
            (1, -1): 0.3,  # Down-Left
            (-1, 1): 0.2,  # Up-Right
            (-1, -1): 0.1, # Up-Left
        }

    def score(self, di: int, dj: int) -> float:
        return self.bias.get((di, dj), 0.0)

    def update_from_observations(self, coords: list[str]):
        """Update bias using a sequence of algebraic coordinates like ['g6','g7','f8'].
        Interprets one-step moves; increases counts for observed directions.
        """
        if not coords:
            return
        cols = "abcdefgh"
        def to_ij(coord: str) -> tuple[int, int]:
            x = coord[0].lower()
            y = int(coord[1:])
            j = cols.index(x)
            i = 8 - y
            return i, j
        for a, b in zip(coords, coords[1:]):
            i1, j1 = to_ij(a)
            i2, j2 = to_ij(b)
            di = max(-1, min(1, i2 - i1))
            dj = max(-1, min(1, j2 - j1))
            if di == 0 and dj == 0:
                continue
            self.bias[(di, dj)] = self.bias.get((di, dj), 0.0) + 1.0


# Global movement model instance (can be updated at runtime)
movement_model = MovementModel()


def get_neighbors_by_mode(radar: list[list['Node']], i: int, j: int, obstacle_symbol: str, mode: str) -> list['Node']:
    rows, cols = len(radar), len(radar[0])
    res = []

    # Cardinal directions (order is initial, will be re-ordered by movement_model)
    candidates = [
        (i + 1, j),  # Down
        (i - 1, j),  # Up
        (i, j - 1),  # Left
        (i, j + 1),  # Right
    ]

    if mode == "diag_corner_cutting" or mode == "diag_no_corner_cutting":
        # Diagonals
        diag = [
            (i + 1, j + 1),  # Down-Right
            (i + 1, j - 1),  # Down-Left
            (i - 1, j + 1),  # Up-Right
            (i - 1, j - 1),  # Up-Left
        ]
        if mode == "diag_corner_cutting":
            # No gating; add all diagonals if in-bounds
            candidates.extend(diag)
        else:
            # No corner cutting: only allow diagonal if both adjacent cardinals are free
            for di, dj in diag:
                if not in_bounds(di, dj, rows, cols):
                    continue
                ai, aj = di, j      # vertical adjacent
                bi, bj = i, dj      # horizontal adjacent
                if in_bounds(ai, aj, rows, cols) and in_bounds(bi, bj, rows, cols):
                    if radar[ai][aj].value != obstacle_symbol and radar[bi][bj].value != obstacle_symbol:
                        candidates.append((di, dj))

    # Filter viable moves (in bounds and not obstacle)
    viable: list[tuple[int, int]] = []
    for ni, nj in candidates:
        if in_bounds(ni, nj, rows, cols) and radar[ni][nj].value != obstacle_symbol:
            viable.append((ni, nj))

    # Sort viable moves by learned bias (higher score first). Tie-break by original order via stable sort.
    viable.sort(key=lambda pos: movement_model.score(pos[0]-i, pos[1]-j), reverse=True)

    # Map to nodes in the learned order
    for ni, nj in viable:
        res.append(radar[ni][nj])
    return res


def bfs_shortest_path(start: 'Node', goal: 'Node') -> list['Node']:
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    while queue:
        node = queue.popleft()
        if node is goal:
            # reconstruct
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path
        for neigh in node.childrens:
            if neigh not in visited:
                visited.add(neigh)
                parent[neigh] = node
                queue.append(neigh)
    return []


def idx_to_coord(i: int, j: int) -> str:
    # Grid is constructed from top (row 0) = y=7 to bottom (row 7) = y=0
    # Columns a..h map to j=0..7
    cols = "abcdefgh"
    # Convert internal i (0..7 top->bottom) to board y (1..8 bottom->top)
    y = 8 - i
    x = cols[j]
    return f"{x}{y}"


def coord_to_idx(coord: str) -> tuple[int, int]:
    cols = "abcdefgh"
    x = coord[0].lower()
    y = int(coord[1:])
    j = cols.index(x)
    i = 8 - y
    return i, j


def add_stops(first_radar: str, stops: list[str]) -> str:
    """Merge first_radar with a list of additional stop radars.
    Priority per cell: '$' > '#' > '^' > 'p' > '0'.
    Returns a compact symbol-only radar with '|' separators, compatible with our parser.
    """
    # Normalize stop markers: convert any '^' in stops to p, leave base '^' intact
    norm_stops = [s.replace("^", ENEMY_SHIP_STOP_SYMBOL) for s in stops]

    base_rows = first_radar.split("|")
    stop_rows_list = [s.split("|") for s in norm_stops]
    lengths = [len(base_rows)] + [len(sr) for sr in stop_rows_list]
    n = min(lengths)

    out_rows: list[str] = []
    for idx in range(n):
        if not base_rows[idx]:
            continue
        # Extract symbols for the base row
        base_syms = re.findall(r"[0\#\^\$]", base_rows[idx])
        if not base_syms:
            continue
        # Extract symbols for each stop row (allow p)
        stop_syms_rows: list[list[str]] = []
        for sr in stop_rows_list:
            if idx >= len(sr) or not sr[idx]:
                continue
            stop_syms_rows.append(re.findall(r"[0\#\^\$p]", sr[idx]))

        # Determine min width across all rows for safe zipping
        widths = [len(base_syms)] + [len(x) for x in stop_syms_rows]
        if not widths:
            continue
        w = min(widths)

        merged_syms: list[str] = []
        for k in range(w):
            symbols = [base_syms[k]]
            for row_syms in stop_syms_rows:
                if k < len(row_syms):
                    symbols.append(row_syms[k])
            # Apply priority: $ > # > ^ > p > 0
            if '$' in symbols:
                merged_syms.append('$')
            elif '#' in symbols:
                merged_syms.append('#')
            elif '^' in symbols:
                merged_syms.append('^')
            elif ENEMY_SHIP_STOP_SYMBOL in symbols:
                merged_syms.append(ENEMY_SHIP_STOP_SYMBOL)
            else:
                merged_syms.append('0')
        out_rows.append("".join(merged_syms))

    return "|".join(out_rows) + "|"


def parse_radar(cripted_radar: str, stops: list[str] = [], color: bool = True):

    columns = ["a", "b", "c", "d", "e", "f", "g", "h"]

    origen_symbol = "^" # Enemy ship
    destination_symbol = "#" # Hope ship
    obstacle_symbol = "$"
    origen_ref = None
    destination_ref = None

    radar: list[list[Node]] = []
    for i, row in enumerate(cripted_radar.split("|")[:-1][::-1]):
        matches = re.findall(r'[0\#\^\$p]', row)  # list of all '0', '#', '^', '$', 'p' in this row
        row_node: list[Node] = []
        for j, match in enumerate(matches):
            # y should be top-based index. We reversed rows above, so map back: y = total_rows - 1 - i
            node = Node(value=match, childrens=[], x=columns[j], y=i)

            # Keep a reference from the origin and the destination.
            if match == origen_symbol:
                origen_ref = node
            elif match == destination_symbol:
                destination_ref = node

            row_node.append(node)
        radar.append(row_node)
        # print(" ".join(matches))

    # Build three graphs (childrens) according to movement mode
    # We assume enemy seeks the fastest path avoiding obstacles, allowing diagonals
    # but without corner cutting (typical realistic constraint)
    modes = [
        ("cardinal_only", "Only horizontal/vertical"),
        ("diag_corner_cutting", "Diagonals allowed (corner cutting)"),
        ("diag_no_corner_cutting", "Diagonals allowed (no corner cutting)"),
    ]

    # Helper: extract ordered waypoint coordinates (i,j) from stop snapshots
    def extract_waypoints_from_stops(stops_snaps: list[str]) -> list[tuple[int, int]]:
        waypoints: list[tuple[int, int]] = []
        if not stops_snaps:
            return waypoints
        for snap in stops_snaps:
            # Iterate rows in the same reversed manner as radar parsing
            found: tuple[int, int] | None = None
            for i_idx, row in enumerate(snap.split("|")[:-1][::-1]):
                matches = re.findall(r'[0\#\^\$p]', row)
                for j_idx, ch in enumerate(matches):
                    if ch == '^':
                        found = (i_idx, j_idx)
                        break
                if found is not None:
                    break
            if found is not None:
                waypoints.append(found)
        return waypoints

    # For each mode, rewire childrens, run multi-segment BFS via waypoints, and print grid overlay
    for mode_key, mode_label in modes:
        for i, row in enumerate(radar):
            for j, cell in enumerate(row):
                cell.childrens = get_neighbors_by_mode(radar, i, j, obstacle_symbol, mode_key)

        # Build ordered waypoints from stops and map to nodes
        waypoint_coords = extract_waypoints_from_stops(stops)
        waypoint_nodes: list[Node] = []
        for (wi, wj) in waypoint_coords:
            if 0 <= wi < len(radar) and 0 <= wj < len(radar[wi]):
                waypoint_nodes.append(radar[wi][wj])

        # Run multi-segment BFS: origin -> each waypoint -> destination
        segments: list[list[Node]] = []
        ok = True
        cur = origen_ref
        for wp in waypoint_nodes + [destination_ref]:
            seg = bfs_shortest_path(cur, wp)
            if not seg:
                ok = False
                break
            if segments:
                # avoid duplicating joint node
                segments.append(seg[1:])
            else:
                segments.append(seg)
            cur = wp
        path: list[Node] = []
        if ok:
            for seg in segments:
                path.extend(seg)
        else:
            # fallback to direct if multi-segment fails
            path = bfs_shortest_path(origen_ref, destination_ref)

        # Print header and grid with path overlay
        print(f"Mode: {mode_label}")
        path_set = set(path)
        print("x/y", " ".join(columns))
        for i, row in enumerate(radar):
            print(9 - (i+1), end=" | ")
            for node in row:
                if node in path_set and node not in [origen_ref, destination_ref] and node.value != ENEMY_SHIP_STOP_SYMBOL:
                    ch = colorize('*', color)
                    print(ch, end=" ")
                else:
                    ch = colorize(node.value, color)
                    print(ch, end=" ")
            print()
        print()

        # Compute stop-informed metrics and predictions
        if path:
            # 1) Print next up to 4 positions (simple preview)
            next_steps = path[1:5]  # skip origin
            coords = []
            for n in next_steps:
                i_idx = n.y
                j_idx = columns.index(n.x)
                coords.append(idx_to_coord(i_idx, j_idx))
            print("Predicted next positions (up to 4 turns):", ", ".join(coords) if coords else "<none>")

            # 2) Segment lengths between origin and stops (then between stops)
            segment_lengths: list[int] = []
            cumulative_lengths: list[int] = []
            points: list[Node] = [origen_ref] + waypoint_nodes
            total = 0
            if len(points) > 1:
                for a, b in zip(points, points[1:]):
                    seg = bfs_shortest_path(a, b)
                    moves = max(0, len(seg) - 1)
                    segment_lengths.append(moves)
                    total += moves
                    cumulative_lengths.append(total)

                # Print per-segment and cumulative from origin
                print("Segment lengths (origin->stop1, stop1->stop2, ...):", segment_lengths)
                print("Cumulative lengths from origin to each stop:", cumulative_lengths)

                # 3) Average segment length
                avg = round(sum(segment_lengths) / len(segment_lengths)) if segment_lengths else 0
                print("Average segment length:", avg)

                # 4) From last stop, jump 'avg' steps along the current full path and report that coordinate
                last_stop = waypoint_nodes[-1]
                try:
                    idx_last = path.index(last_stop)
                    idx_target = min(len(path) - 1, idx_last + max(0, avg))
                    target_node = path[idx_target]
                    tcoord = idx_to_coord(target_node.y, columns.index(target_node.x))
                    print("Predicted by avg-jump from last stop:", tcoord)
                except ValueError:
                    print("Last stop not found in path; cannot compute avg-jump prediction.")
            else:
                # No intermediate points: divide the full path into five and jump one-fifth from origin
                total_moves = max(0, len(path))
                step = max(1, round(total_moves / 5)) if total_moves > 0 else 0
                if step > 0:
                    idx_target = min(len(path) - 1, step)
                    target_node = path[idx_target]
                    tcoord = idx_to_coord(target_node.y, columns.index(target_node.x))
                    print("Predicted by 1/5 path jump from origin:", tcoord)
                else:
                    print("Insufficient path to compute 1/5 jump prediction.")

            print()

            
    # Done printing all modes
    

if __name__ == "__main__":

    radar_a = "a01b^1c01d01e01f01g01h01|a02b02c02d$2e02f02g02h02|a03b03c$3d03e03f03g03h03|a04b04c$4d04e04f04g04h04|a05b05c05d05e05f05g05h05|a06b06c06d$6e06f06g06h06|a07b07c07d07e07f07g07h07|a08b08c08d08e#8f08g08h08|"
    stops = [
        "a01b01c01d01e01f01g01h01|a02b02c02d$2e02f02g02h02|a^3b03c$3d03e03f03g03h03|a04b04c$4d04e04f04g04h04|a05b05c05d05e05f05g05h05|a06b06c06d$6e06f06g06h06|a07b07c07d07e07f07g07h07|a08b08c08d08e#8f08g08h08|",
        "a01b01c01d01e01f01g01h01|a02b02c02d$2e02f02g02h02|a03b03c$3d03e03f03g03h03|a04b04c$4d04e04f04g04h04|a05b^5c05d05e05f05g05h05|a06b06c06d$6e06f06g06h06|a07b07c07d07e07f07g07h07|a08b08c08d08e#8f08g08h08|",
    ]


    merged = add_stops(radar_a, stops)
    parse_radar(merged, stops=stops)
