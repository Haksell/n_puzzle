import pyglet

window = pyglet.window.Window()
label = pyglet.text.Label(
    "Hello, world!",
    font_size=36,
    x=window.width // 2,
    y=window.height // 2,
    anchor_x="center",
    anchor_y="center",
)


@window.event
def on_draw():
    window.clear()
    label.draw()


def launch_gui(puzzle, solution):
    print(puzzle, solution)
    pyglet.app.run()
