'''
Simple gridworld with two different paths to goal

Key for ascii art
# - wall
O - player location
X - goal state

goal-state teleports the player to start-state
episodes never end

Reward:
    moving into goal state gives 50
    any action give 1
'''

import curses
import numpy as np
from pycolab import ascii_art
from pycolab import human_ui
from pycolab.prefab_parts import sprites as prefab_sprites


GRID_WORLD = ['###########',
              '#         #',
              '# O ##  X #',
              '#   ##    #',
              '#   ##    #',
              '#         #',
              '#         #',
              '#         #',
              '###########',]


def get_params():
    '''
    gives the parameter of the environment
    1. number of actions
    2. number of states
    3. shape of gridworld
    '''
    params = {
        'num_actions': 4,
        'num_states' : len(GRID_WORLD) * len(GRID_WORLD[0]),
        'shape' : (len(GRID_WORLD), len(GRID_WORLD[0]))
        }
    return params


def make_game():
    '''
    builds the game and returns the engine
    '''
    return ascii_art.ascii_art_to_game(
        GRID_WORLD,
        what_lies_beneath=' ',  # space character
        sprites={'O': PlayerSprite})


class PlayerSprite(prefab_sprites.MazeWalker):
    '''
    Class for player

    Defines movements and associated rewards
    '''

    def __init__(self, corner, position, character):
        '''
        initialize as per superclass instructions and make walls impassable
        '''
        super(PlayerSprite, self).__init__(
            corner, position, character, impassable=['#', 'X'])

    def update(self, actions, board, layers, backdrop, things, the_plot):
        del backdrop, things, layers  # Unused
        # Initialize obstruction
        obstruction = None
        if actions == 0:    # go west
            obstruction = self._west(board, the_plot)
        elif actions == 1:  # go east
            obstruction = self._east(board, the_plot)
        elif actions == 2:  # go north
            obstruction = self._north(board, the_plot)
        elif actions == 3:  # go south
            obstruction = self._south(board, the_plot)
        elif actions == 4:  # stay (for human player)
            self._stay(board, the_plot)
        elif actions == 5:    # quit (for termination)
            the_plot.terminate_episode()
        if obstruction == 'X': # if moving to goal state, reward and teleport
            the_plot.add_reward(50)
            self._teleport((2, 2))


def main():
    '''
    C-style main function
    '''

    # Build the game
    game = make_game()

    # Create user interface
    user_interface = human_ui.CursesUi(
        keys_to_actions={curses.KEY_LEFT: 0,
                         curses.KEY_RIGHT: 1,
                         curses.KEY_UP: 2,
                         curses.KEY_DOWN: 3,
                         -1: 4,  # for dummy stayput action
                         'q': 5, 'Q': 5},  # to exit
        delay=200)

    # Run the game
    user_interface.play(game)


if __name__ == '__main__':
    main()
