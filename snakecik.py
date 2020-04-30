import pyglet
import random
import time
from pathlib import Path

red = pyglet.image.load('apple.png')
green = pyglet.image.load('green.png')
batch = pyglet.graphics.Batch()


TILES_DIRECTORY = Path('snake-tiles')

TILE_SIZE = [64, 64]
TILE = 64
WINDOW_SIZE = [640, 640]


label = pyglet.text.Label(color=(255, 191, 0, 255), x=1/2*TILE_SIZE[0], y=1/2*TILE_SIZE[1], font_size=36)  # score label
gameover = pyglet.text.Label(color=(255, 191, 0, 255), x=TILE_SIZE[0], y=3*TILE_SIZE[1], font_size=60)  # gameover label


class State:
    def __init__(self):
        self.speed = 6  # beginning speed of snake
        self.snake = [(0, 0), (1, 0)]  # how snake looks before eating apples
        self.snake_direction = 0, 1  # beginning direction of snake
        self.width = 10
        self.height = 10
        self.score = 0  # number of apples snake ate
        self.snake_alive = True  # snake is in mode alive from begining
        self.food = []
        self.add_food()  # two apples at the beginning of the game
        self.add_food()

    def move(self):
        """
        Moving with snake
        """
        old_x, old_y = self.snake[-1]
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y
        new_head = new_x, new_y
        print(new_head, 'position of new head in snake')

        # what happens when snake goes of the game area
        if new_x < 0 or new_y < 0 or new_x >= self.width or new_y >= self.height:
            self.snake_alive = False
            gameover.text = ("GAME OVER")

        if new_head in self.snake:
            self.snake_alive = False
            gameover.text = ("GAME OVER")

        if not self.snake_alive:
            return
        self.snake.append(new_head)
        if new_head in self.food:
            self.food.remove(new_head)
            self.score += 1  # after eating apple, score +1
            self.change_speed()
            self.add_food()
        else:
            del self.snake[0]

    def direction(self, direction_a, direction_b):
        """
        Choosing right tile/picture of snake
        """
        if direction_a is None or direction_b is None:
            return 'end'
        (course_x1, course_y1) = direction_a
        (course_x2, course_y2) = direction_b
        if course_x1 == course_x2 - 1:
            return 'left'
        elif course_x1 == course_x2 + 1:
            return 'right'
        elif course_y1 == course_y2 - 1:
            return 'bottom'
        elif course_y1 == course_y2 + 1:
            return 'top'
            return 'end'
        # elif not self.snake_alive:
        #     return 'dead'

    def add_food(self):
        """
        Add apple to game after snake eates one
        """
        while True:
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            print(position, 'position of apple')
            if (position not in self.snake) and (position not in self.food):
                self.food.append(position)
                return

    def change_speed(self):
        """
        Changes speed (+1) of snake after every third apple snake eates
        """
        if self.score in range(0, 100, 3):
            self.speed = self.speed + 1
            pyglet.clock.unschedule(move)
            pyglet.clock.schedule_interval(move, 1/self.speed)

    def gameover(self):
        """
        When snake not alive, draw gameover text
        """
        if not self.snake_alive:
            gameover.draw()
            pyglet.clock.unschedule(move)
            return True
        return False


snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = pyglet.image.load(path)

# print(snake_tiles)

window = pyglet.window.Window(640, 640)

snakey = State()  # create instance of State class
snakey.width = window.width // TILE
snakey.height = window.height // TILE


@window.event
def on_key_press(key_code, modifier):
    """
    Direction from the keyboard - what happens when you press keyboard
    """
    if key_code == pyglet.window.key.LEFT and snakey.snake_direction != (1, 0):
        snakey.snake_direction = -1, 0
    if key_code == pyglet.window.key.RIGHT and snakey.snake_direction != (-1, 0):
        snakey.snake_direction = 1, 0
    if key_code == pyglet.window.key.DOWN and snakey.snake_direction != (0, 1):
        snakey.snake_direction = 0, -1
    if key_code == pyglet.window.key.UP and snakey.snake_direction != (0, -1):
        snakey.snake_direction = 0, 1


@window.event
def on_draw():
    window.clear()

    # pyglet.gl.glEnable(pyglet.gl.GL_BLEND)  #  better graphics
    # pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    green_image = []
    for direction_a, direction_b, direction_c in zip([None] + snakey.snake, snakey.snake, snakey.snake[1:] + [None]):
        x, y = direction_b
        source = snakey.direction(direction_a, direction_b)
        dest = snakey.direction(direction_c, direction_b)
        print(x, y, source, dest, 'directions')
        green_image.append(pyglet.sprite.Sprite(snake_tiles[source + '-' + dest], x * TILE_SIZE[0], y * TILE_SIZE[1], batch=batch))
    red_image = []
    for x, y in snakey.food:
        red_image.append(pyglet.sprite.Sprite(red, x * TILE_SIZE[0], y * TILE_SIZE[1], batch=batch))

    batch.draw()
    label.text = (str(snakey.score))
    label.draw()
    if snakey.gameover():
        return


def move(dt):
    snakey.move()


pyglet.clock.schedule_interval(move, 1/snakey.speed)
pyglet.app.run()
