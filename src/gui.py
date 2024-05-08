import pyglet
from pyglet.graphics import Batch

MAX_TILE_SIZE = 125
MAX_SCREEN_PROPORTION = 0.7
TILE_MARGIN = 0.05  # TODO: add it on the border
CORRECT_COLOR = (232, 138, 69)
INCORRECT_COLOR = (106, 198, 184)


class GUI(pyglet.window.Window):
    def __init__(self, puzzle):
        self.tile_size = self.__compute_tile_size(puzzle)
        super().__init__(
            width=self.tile_size * puzzle.width,
            height=self.tile_size * puzzle.height,
            caption=f"{len(puzzle)-1}-puzzle",
        )
        self.font_size = self.__compute_font_size(puzzle)
        self.batch = self.__make_batch(puzzle)

    def __compute_tile_size(self, puzzle):
        screen = pyglet.canvas.get_display().get_default_screen()
        return min(
            MAX_TILE_SIZE,
            int(
                min(screen.height / puzzle.height, screen.width / puzzle.width)
                * MAX_SCREEN_PROPORTION
            ),
        )

    def __compute_font_size(self, puzzle):
        max_digits = len(str(puzzle.width * puzzle.height - 1))
        factor = max(0.2, 0.4 - max_digits * 0.04)
        return round(self.tile_size * factor)

    def __make_batch(self, puzzle):
        batch = Batch()
        background_margin = TILE_MARGIN * self.tile_size
        background_size = (1 - 2 * TILE_MARGIN) * self.tile_size
        half_tile = self.tile_size // 2
        for i, number in enumerate(puzzle):
            if number == 0:
                continue
            y, x = divmod(i, puzzle.width)
            pyglet.text.Label(
                str(number),
                font_size=self.font_size,
                x=x * self.tile_size + half_tile,
                y=self.height - (y * self.tile_size + half_tile),
                anchor_x="center",
                anchor_y="center",
                color=(255, 255, 255, 255),  # TODO: better color and font
                batch=batch,
            )
            pyglet.shapes.Rectangle(
                x * self.tile_size + background_margin,
                self.height - (y * self.tile_size + self.tile_size) + background_margin,
                background_size,
                background_size,
                color=CORRECT_COLOR if puzzle.is_correct(i) else INCORRECT_COLOR,
                batch=batch,
            )
        return batch

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def run(self):
        pyglet.app.run()
