from RESOURCES.locale import Locale

from .action_setup import tryCommand
from .world import (
    command_tutorial,
    get_game_over,
    get_player,
    init_player,
)


def main_loop():
    while not get_game_over():
        tryCommand()


def main():
    Locale.set_locale("en_US")
    init_player()
    #get_player().set_name("Adventurer")
    #get_player().set_age(18)
    #get_enemy()
    #command_tutorial()
    main_loop()
