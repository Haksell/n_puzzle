import math
import pyglet
from src.lib import clamp
import time


FONT_NAME = "PoetsenOne"
FONT_FILE = f"{FONT_NAME}-Regular.ttf"
MAX_TILE_SIZE = 125
MAX_SCREEN_PROPORTION = 0.7
TILE_PADDING = 0.05
COLOR_CORRECT = (232, 138, 69)
COLOR_INCORRECT = (106, 198, 184)
KEY_TIMEOUT_INITIAL = 0.4
KEY_TIMEOUT_REPEAT = 0.05

pyglet.font.add_file(FONT_FILE)


# TODO: remove
class DummyPuzzle:
    def __init__(self):
        self.__width = 4
        self.__height = 4
        self.__tiles = list(range(self.__width * self.__height))

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    def __iter__(self):
        yield from self.__tiles

    def __len__(self):
        return len(self.__tiles)

    def is_correct(self, _):
        return __import__("random").choice([False, True])


class GUI(pyglet.window.Window):
    def __init__(self, puzzle, solution):
        self.__puzzle = puzzle
        self.__solution = solution
        self.__tile_size = self.__compute_tile_size()
        self.__padding = round(TILE_PADDING * self.__tile_size)
        self.__position = 0
        super().__init__(
            width=self.__tile_size * puzzle.width + 2 * self.__padding,
            height=self.__tile_size * puzzle.height + 2 * self.__padding,
            caption=self.__get_caption(),
        )
        self.__font_size = self.__compute_font_size()
        self.__batch = self.__make_batch()
        self.__keys = pyglet.window.key.KeyStateHandler()
        self.__left_key_start = self.__right_key_start = self.__left_key_prev = (
            self.__right_key_prev
        ) = 0.0
        self.push_handlers(self.__keys)

    def __compute_tile_size(self):
        screen = pyglet.canvas.get_display().get_default_screen()
        h = screen.height / self.__puzzle.height
        w = screen.width / self.__puzzle.width
        return min(MAX_TILE_SIZE, int(min(h, w) * MAX_SCREEN_PROPORTION))

    def __get_caption(self):
        return (
            f"{len(self.__puzzle)-1}-puzzle ({self.__position}/{len(self.__solution)})"
        )

    def __compute_font_size(self):
        max_digits = len(str(self.__puzzle.width * self.__puzzle.height - 1))
        factor = max(0.2, 0.48 - max_digits * 0.04)
        return round(self.__tile_size * factor)

    def __make_batch(self):
        batch = pyglet.graphics.Batch()
        visible_tile_size = (1 - 2 * TILE_PADDING) * self.__tile_size
        label_offset = self.__tile_size // 2 + self.__padding
        for i, number in enumerate(self.__puzzle):
            if number == 0:
                continue
            y, x = divmod(i, self.__puzzle.width)
            pyglet.text.Label(
                str(number),
                font_size=self.__font_size,
                font_name=FONT_NAME,
                x=x * self.__tile_size + label_offset,
                y=self.height - (y * self.__tile_size + label_offset),
                anchor_x="center",
                anchor_y="center",
                color=(255, 255, 255, 255),
                batch=batch,
            )
            pyglet.shapes.Rectangle(
                x * self.__tile_size + 2 * self.__padding,
                self.height - (y * self.__tile_size + self.__tile_size),
                visible_tile_size,
                visible_tile_size,
                color=COLOR_CORRECT if self.__puzzle.is_correct(i) else COLOR_INCORRECT,
                batch=batch,
            )
        return batch

    @staticmethod
    def __count_repeats(start, end):
        return max(
            0,
            1
            + int(math.floor((end - start - KEY_TIMEOUT_INITIAL) / KEY_TIMEOUT_REPEAT)),
        )

    def __update_keys(self, current_time, key, start, prev):
        if not self.__keys[key]:
            return 0, 0, 0
        elif start == 0.0:
            return current_time, current_time, 1
        else:
            return (
                start,
                current_time,
                self.__count_repeats(start, current_time)
                - self.__count_repeats(start, prev),
            )

    def __update_position(self):
        current_time = time.time()
        self.__left_key_start, self.__left_key_prev, left_repeats = self.__update_keys(
            current_time,
            pyglet.window.key.LEFT,
            self.__left_key_start,
            self.__left_key_prev,
        )
        self.__right_key_start, self.__right_key_prev, right_repeats = (
            self.__update_keys(
                current_time,
                pyglet.window.key.RIGHT,
                self.__right_key_start,
                self.__right_key_prev,
            )
        )
        return (
            self.__position
            if self.__keys[pyglet.window.key.LEFT]
            == self.__keys[pyglet.window.key.RIGHT]
            else clamp(
                self.__position + right_repeats - left_repeats, 0, len(self.__solution)
            )
        )

    def on_draw(self):
        self.__position = self.__update_position()
        self.set_caption(self.__get_caption())
        pyglet.gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        self.clear()
        self.__batch.draw()

    def run(self):
        pyglet.app.run()
