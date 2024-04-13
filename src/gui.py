import tkinter as tk
from .lib import make_goal

# TODO: make the tiles non-clickable
# TODO: animations
# TODO: p5


def __do_move(puzzle, move, size, zero_idx):
    swap_idx = zero_idx + [size, -1, -size, 1][move]
    puzzle[zero_idx], puzzle[swap_idx] = puzzle[swap_idx], puzzle[zero_idx]


def __draw_puzzle(board_frame, tiles, goal, width, height):
    square_size = 100
    for y in range(height):
        for x in range(width):
            tile = tiles[height * y + x]
            goal_tile = goal[height * y + x]
            txt, bg_color = (
                ("", "White")
                if tile == 0
                else (str(tile), "#E88A45" if tile == goal_tile else "#6AC6B8")
            )
            tk.Button(
                board_frame,
                text=txt,
                relief="solid",
                bd=1,
                bg=bg_color,
                font="times 12 bold",
            ).place(
                x=square_size * x,
                y=square_size * y,
                height=square_size,
                width=square_size,
            )


# def __draw_puzzle(board_frame, buttons, tiles, goal, width, height):
#     buttons = []
#     for y in range(height):
#         for x in range(width):
#             tile = tiles[height * y + x]
#             goal_tile = goal[height * y + x]
#             txt, bg_color = (
#                 ("", "White")
#                 if tile == 0
#                 else (str(tile), "#E88A45" if tile == goal_tile else "#6AC6B8")
#             )
#             buttons.append(
#                 tk.Button(
#                     board_frame,
#                     text=txt,
#                     relief="solid",
#                     bd=1,
#                     bg=bg_color,
#                     font="times 12 bold",
#                 )
#             )
#     return buttons


def launch_gui(puzzle, solution):
    pos = 0
    tiles = list(puzzle)
    size = puzzle.height
    goal = make_goal(puzzle.height)

    def go_start():
        nonlocal pos
        pos = 0
        tiles = list(puzzle)
        __draw_puzzle(board_frame, tiles, goal, size, size)

    def go_previous():
        nonlocal pos
        if pos > 0:
            pos -= 1
            __do_move(tiles, solution[pos].opposite(), size, tiles.index(0))
            __draw_puzzle(board_frame, tiles, goal, size, size)

    def play():
        pass

    def go_next():
        nonlocal pos
        if pos < len(solution):
            __do_move(tiles, solution[pos], size, tiles.index(0))
            pos += 1
            __draw_puzzle(board_frame, tiles, goal, size, size)

    def go_end():
        nonlocal pos
        pos = len(solution)
        tiles = goal.copy()
        __draw_puzzle(board_frame, tiles, goal, size, size)

    root = tk.Tk()
    root.title("n_puzzle")
    root.geometry("600x600+0+0")
    root.resizable(False, False)

    top_frame = tk.Frame(root, width=600, height=100, bg="light green")
    top_frame.pack_propagate(False)
    top_frame.pack(fill=tk.X)

    button_width = 10
    button_height = 2
    padx = 10

    tk.Button(
        top_frame,
        text="⏮️",
        width=button_width,
        height=button_height,
        command=go_start,
    ).pack(side=tk.LEFT, padx=padx)
    tk.Button(
        top_frame,
        text="⏪",
        width=button_width,
        height=button_height,
        command=go_previous,
    ).pack(side=tk.LEFT, padx=padx)
    tk.Button(
        top_frame,
        text="▶️",
        width=button_width,
        height=button_height,
        command=play,
    ).pack(side=tk.LEFT, padx=padx)
    tk.Button(
        top_frame,
        text="⏩",
        width=button_width,
        height=button_height,
        command=go_next,
    ).pack(side=tk.LEFT, padx=padx)
    tk.Button(
        top_frame,
        text="⏭️",
        width=button_width,
        height=button_height,
        command=go_end,
    ).pack(side=tk.LEFT, padx=padx)

    bottom_frame = tk.Frame(root, width=600, height=500, bg="light steel blue")
    bottom_frame.pack(fill=tk.X)

    board_frame = tk.Frame(
        bottom_frame,
        width=400 + 2,
        height=400 + 2,
        relief="solid",
        bd=1,
        bg="lemon chiffon",
    )
    board_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    __draw_puzzle(board_frame, puzzle, goal, size, size)
    root.mainloop()
