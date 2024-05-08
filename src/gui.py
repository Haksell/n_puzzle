import pyglet
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch

"""
TODO: remove
Dummy Puzzle class to test various widths and heights.

class Puzzle:
    def __init__(self):
        self.__width = 32
        self.__height = 32
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
"""


class GUI(pyglet.window.Window):
    def __init__(self, puzzle):
        self.tile_size = self.__compute_tile_size(puzzle)
        super().__init__(
            width=self.tile_size * puzzle.width,
            height=self.tile_size * puzzle.height,
            caption="N-puzzle",
        )
        self.batch = Batch()
        self.font_size = self.__compute_font_size(puzzle)
        self.tiles = self.__make_tiles(puzzle)

    def __compute_tile_size(self, puzzle):
        display = pyglet.canvas.get_display()
        screen = display.get_default_screen()
        return min(
            125,
            int(min(screen.height / puzzle.height, screen.width / puzzle.width) * 0.7),
        )

    def __compute_font_size(self, puzzle):
        max_digits = len(str(puzzle.width * puzzle.height - 1))
        factor = max(0.2, 0.4 - max_digits * 0.04)
        return round(self.tile_size * factor)

    def __make_tiles(self, puzzle):
        tiles = []
        half_tile = self.tile_size // 2
        for i, number in enumerate(puzzle):
            if number == 0:
                continue
            y, x = divmod(i, puzzle.width)
            label = pyglet.text.Label(
                str(number),
                font_size=self.font_size,
                x=x * self.tile_size + half_tile,
                y=self.height - (y * self.tile_size + half_tile),
                anchor_x="center",
                anchor_y="center",
                batch=self.batch,
            )
            tiles.append(label)
        return tiles

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def run(self):
        pyglet.app.run()
