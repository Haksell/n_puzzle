import pyglet
from pyglet.graphics import Batch


MAX_TILE_SIZE = 125
MAX_SCREEN_PROPORTION = 0.7
TILE_PADDING = 0.05
COLOR_CORRECT = (232, 138, 69)
COLOR_INCORRECT = (106, 198, 184)


class GUI(pyglet.window.Window):
    def __init__(self, puzzle):
        self.__tile_size = self.__compute_tile_size(puzzle)
        self.__padding = round(TILE_PADDING * self.__tile_size)
        super().__init__(
            width=self.__tile_size * puzzle.width + 2 * self.__padding,
            height=self.__tile_size * puzzle.height + 2 * self.__padding,
            caption=f"{len(puzzle)-1}-puzzle",
        )
        self.__font_size = self.__compute_font_size(puzzle)
        self.__batch = self.__make_batch(puzzle)

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
        return round(self.__tile_size * factor)

    def __make_batch(self, puzzle):
        batch = Batch()
        visible_tile_size = (1 - 2 * TILE_PADDING) * self.__tile_size
        half_tile = self.__tile_size // 2
        for i, number in enumerate(puzzle):
            if number == 0:
                continue
            y, x = divmod(i, puzzle.width)
            pyglet.text.Label(
                str(number),
                font_size=self.__font_size,
                # TODO: better font
                x=x * self.__tile_size + half_tile + self.__padding,
                y=self.height - (y * self.__tile_size + half_tile + self.__padding),
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
                color=COLOR_CORRECT if puzzle.is_correct(i) else COLOR_INCORRECT,
                batch=batch,
            )
        return batch

    def on_draw(self):
        pyglet.gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        self.clear()
        self.__batch.draw()

    def run(self):
        pyglet.app.run()
