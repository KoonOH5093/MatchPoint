import time

import numpy as np

from game import ConsoleGame

game = ConsoleGame('Map/B.txt')
game.render_answer()

input('render answer map')



game.clear()
answer_actions = np.argwhere(game.answer_map, )[:, ::-1]
for y in range(8):
    for x in range(8):
        result, game = game.paint(x, y)
        print(f'paint at {x},{y}\tresult: {result} {game}')
        game.render()
        time.sleep(0.5)
print('game result', game.check_result())
