import sys
from src import Move

# TODO: just cycle when 2x2


def incremental(puzzle, _):
    solution = []
    pw = puzzle.width
    gzy, gzx = divmod(puzzle.goal_pos[0], pw)
    minx = miny = 0
    maxx, maxy = pw - 1, puzzle.height - 1
    while minx + 1 < maxx or miny + 1 < maxy:
        dl = gzx - minx
        dr = maxx - gzx
        dt = gzy - miny
        db = maxy - gzy
        best = max(dl, dr, dt, db)
        if best == dt:
            line = puzzle.goal[miny * pw : (miny + 1) * pw][minx : maxx + 1]
            print("row", miny, line)
            miny += 1
        elif best == dr:
            line = puzzle.goal[maxx::pw][miny : maxy + 1]
            print("col", maxx, line)
            maxx -= 1
        elif best == db:
            line = puzzle.goal[maxy * pw : (maxy + 1) * pw][minx : maxx + 1]
            print("row", maxy, line)
            maxy -= 1
        else:
            ONE = "DLURRDLURRDL"
            THREE = "ULLLDRRULDRRUL"
            return [
                {"U": Move.UP, "R": Move.RIGHT, "D": Move.DOWN, "L": Move.LEFT}[c]
                for c in ONE + THREE
            ]
            # line = puzzle.goal[minx::pw][miny : maxy + 1]
            # print("col", minx, line)
            # for y in range(miny, maxy - 1):
            #     num = puzzle.goal[y * pw + minx]
            #     zeroy, zerox = divmod(puzzle.index(0), puzzle.width)
            #     numy, numx = divmod(puzzle.index(num), puzzle.width)
            #     print(num, ":", (numy, numx), "to", (y, minx), "using", (zeroy, zerox))
            #     return solution
            # print(puzzle.goal[(maxy - 1) * pw + minx], puzzle.goal[maxy * pw + minx])
            # minx += 1
    return solution


"""
DLURRDLURR
"""
