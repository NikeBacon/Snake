import pyglet
import random
from pathlib import Path

red = pyglet.image.load('apple.png')
green = pyglet.image.load('green.png')
batch = pyglet.graphics.Batch()


TILES_DIRECTORY = Path('snake-tiles')

TILE_SIZE = [64, 64]
TILE = 64
WINDOW_SIZE = [640, 640]


label = pyglet.text.Label(color=(255, 191, 0, 255), x=1/2*TILE_SIZE[0], y=1/2*TILE_SIZE[1], font_size=36)
gameover = pyglet.text.Label(color=(255, 191, 0, 255), x=TILE_SIZE[0], y=3*TILE_SIZE[1], font_size=60)


class State:
    def __init__(self):
        self.snake = [(0, 0), (1, 0)]
        self.snake_direction = 0, 1
        self.width = 10
        self.height = 10
        self.counter = 0
        self.snake_alive = True
        self.speed = 6
        self.food = []
        self.add_food()
        self.add_food()

    def move(self):
        # global SPEED

        if not self.snake_alive:
            return
        old_x, old_y = self.snake[-1]
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y
        new_head = new_x, new_y

        # Kontrola vylezení z hrací plochy
        if new_x < 0:
            self.snake_alive = False
            gameover.text = ("GAME OVER")
        if new_y < 0:
            self.snake_alive = False
            gameover.text = ("GAME OVER")
        if new_x >= self.width:
            self.snake_alive = False
            gameover.text = ("GAME OVER")
        if new_y >= self.height:
            self.snake_alive = False
            gameover.text = ("GAME OVER")
        if new_head in self.snake:
            self.snake_alive = False
            gameover.text = ("GAME OVER")

        self.snake.append(new_head)
        if new_head in self.food:
            self.food.remove(new_head)
            self.counter += 1
            self.add_food()
        else:
            del self.snake[0]

    def add_food(self):
        while True:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            print(position)
            if (position not in self.snake) and (position not in self.food):
                self.food.append(position)
                # break
                return

    def speed(self):
        if self.counter >= 3:
            pyglet.clock._default._current_interval_item.interval = self.speed + 3
        elif self.counter >= 6:
            pyglet.clock._default._current_interval_item.interval = self.speed + 6
        else:
            pyglet.clock._default._current_interval_item.interval = self.speed + 9


snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = pyglet.image.load(path)

print(snake_tiles)

window = pyglet.window.Window(640, 640)

state = State()
state.width = window.width // TILE
state.height = window.height // TILE


@window.event
def on_key_press(key_code, modifier):
    if key_code == pyglet.window.key.LEFT:
        state.snake_direction = -1, 0
    if key_code == pyglet.window.key.RIGHT:
        state.snake_direction = 1, 0
    if key_code == pyglet.window.key.DOWN:
        state.snake_direction = 0, -1
    if key_code == pyglet.window.key.UP:
        state.snake_direction = 0, 1


@window.event
def on_draw():
    window.clear()
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    green_image = []
    for x, y in state.snake:
        source = 'end'
        dest = 'end'
        if dest == 'end' and not state.snake_alive:
            dest = 'dead'
        # green_image = pyglet.sprite.Sprite(green, x * TILE_SIZE[0], y * TILE_SIZE[1], batch=batch)
        green_image.append(pyglet.sprite.Sprite(snake_tiles[source + '-' + dest], x * TILE_SIZE[0], y * TILE_SIZE[1], batch=batch))
    red_image = []
    for x, y in state.food:
        red_image.append(pyglet.sprite.Sprite(red, x * TILE_SIZE[0], y * TILE_SIZE[1], batch=batch))
    batch.draw()
    label.text = (str(state.counter))    # update counter
    label.draw()
    gameover.draw()


def move(dt):
    state.move()


pyglet.clock.schedule_interval(move, 1/state.speed)
pyglet.app.run()
