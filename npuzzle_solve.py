import argparse
from src import heuristics, solvers
from src.Puzzle import Puzzle
from src.hash_puzzle import compressed, uncompressed
from src.solvers import Move
import time
import tkinter as tk


def __parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Filename of the puzzle")
    parser.add_argument(
        "--compress", action="store_true", help="Compress the puzzle representation"
    )
    parser.add_argument("--gui", action="store_true", help="Open a window")
    # TODO: refactor heurstic and solver code
    heuristic_names = [h.__name__ for h in heuristics.HEURISTICS]
    parser.add_argument(
        "--heuristic",
        type=str,
        choices=heuristic_names,
        default=heuristic_names[0],
        help=f"Type of heuristic to use. Defaults to {heuristic_names[0]}.",
    )
    solver_names = [h.__name__ for h in solvers.SOLVERS]
    parser.add_argument(
        "--solver",
        type=str,
        choices=solver_names,
        default=solver_names[0],
        help=f"Type of solver to use. Defaults to {solver_names[0]}.",
    )
    args = parser.parse_args()
    puzzle = Puzzle.from_file(args.filename)
    hash_pair = compressed if args.compress else uncompressed
    heuristic = next(h for h in heuristics.HEURISTICS if h.__name__ == args.heuristic)
    solver = next(s for s in solvers.SOLVERS if s.__name__ == args.solver)
    return puzzle, hash_pair, heuristic, solver, args.gui


def __launch_gui(puzzle, solution):
    tiles = list(puzzle)
    root = tk.Tk()
    root.title("n_puzzle")
    root.geometry("600x600+100+50")
    root.resizable(False, False)
    bd = None
    playable = False

    top_fr = tk.Frame(root, width=600, height=100, bg="light green")
    top_fr.pack(fill=tk.X)

    hdg = tk.Label(
        top_fr,
        text="  15 PUZZLE GAME  ",
        font="arial 22 bold",
        fg="Navy Blue",
        bg="white",
    )
    hdg.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    play_btn = tk.Button(
        top_fr,
        text="New \nGame",
        bd=5,
        bg="PaleGreen4",
        fg="White",
        font="times 12 bold",
        # command=new_game,
    )
    play_btn.place(relx=0.92, rely=0.5, anchor=tk.E)

    btm_fr = tk.Frame(root, width=600, height=500, bg="light steel blue")
    btm_fr.pack(fill=tk.X)

    bd_fr = tk.Frame(
        btm_fr,
        width=400 + 2,
        height=400 + 2,
        relief="solid",
        bd=1,
        bg="lemon chiffon",
    )
    bd_fr.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    if playable:
        btn_state = "normal"
    else:
        btn_state = "disable"

    objh = 100
    objw = 100
    objx = 0
    objy = 0

    for r in range(4):
        for c in range(4):
            tile = tiles[4 * r + c]
            if tile == 0:
                txt = ""
                bg_color = "White"
            else:
                txt = str(tile)
                bg_color = "RosyBrown1"
            game_btn = tk.Button(
                bd_fr,
                text=txt,
                relief="solid",
                bd=1,
                bg=bg_color,
                font="times 12 bold",
                state=btn_state,
                # command=lambda x=nm: clicked(x),
            )
            game_btn.place(x=objx, y=objy, height=objh, width=objw)

            # sq = bd.get_square(r, c)
            # sq.set_btn(game_btn)

            objx = objx + objw
        objx = 0
        objy = objy + objh

    root.mainloop()


def __main():
    puzzle, hash_pair, heuristic, solver, gui = __parse_args()
    t0 = time.time()
    # solution = solver(puzzle, heuristic, hash_pair)
    solution = [
        Move.DOWN,
        Move.LEFT,
        Move.DOWN,
        Move.RIGHT,
        Move.RIGHT,
        Move.UP,
        Move.LEFT,
        Move.DOWN,
        Move.RIGHT,
        Move.DOWN,
        Move.RIGHT,
        Move.UP,
        Move.UP,
        Move.LEFT,
        Move.DOWN,
        Move.DOWN,
        Move.LEFT,
        Move.LEFT,
        Move.UP,
        Move.RIGHT,
        Move.RIGHT,
        Move.DOWN,
        Move.LEFT,
        Move.LEFT,
        Move.UP,
        Move.RIGHT,
        Move.UP,
        Move.RIGHT,
        Move.UP,
        Move.LEFT,
        Move.DOWN,
        Move.LEFT,
        Move.UP,
        Move.RIGHT,
        Move.RIGHT,
        Move.RIGHT,
        Move.DOWN,
        Move.LEFT,
        Move.LEFT,
        Move.LEFT,
        Move.DOWN,
        Move.RIGHT,
        Move.RIGHT,
        Move.RIGHT,
        Move.UP,
        Move.LEFT,
        Move.DOWN,
        Move.DOWN,
        Move.RIGHT,
        Move.UP,
        Move.LEFT,
        Move.LEFT,
        Move.UP,
        Move.RIGHT,
    ]
    print(list(puzzle))
    print(", ".join("Move." + move.name for move in solution))
    print(
        "".join(move.name[0] for move in solution),
        len(solution),
        f"{time.time() - t0:.3f}s",
        solver.__name__,
        heuristic.__name__,
        hash_pair.name,
    )
    if gui:
        __launch_gui(puzzle, solution)


if __name__ == "__main__":
    __main()
