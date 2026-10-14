from time import sleep
from uuid import uuid4

from ATTRIBUTE.attribute_map import AttributeMap
from ENTITY.entity import Entity
from ENTITY.player import Player
from ENTITY.RACE.gender import Gender
from ENTITY.RACE.race import Race
from ENTITY.RACE.race_instance import RaceInstance
from ENTITY.RACE.races import Races

from .parse import inform, wait_for_integer, wait_for_string, whisper

_player: Player = Player(uuid4(), AttributeMap(),
                         RaceInstance(Races.Human, Gender.Male))


def notify_level_up(entity: Entity):
    print("You have leveled up to level {}!".format(entity.level))
    if entity.experience_ratio < 1:
        print("\t\33[2;3m{} XP to next level\33[0m".format(
            max(entity.experience_to_level - entity.experience, 1)))
        print("\t\33[2;3mRestored to full HP, MP, and STA")
        print("\tYou now have {} skill points\33[0m".format(
            entity.skill_points))
        print()


_player.add_level_listener(lambda _e: notify_level_up(_e))

_fight_mode: bool = False
turn = 0

exited: bool = False


def end_game():
    global exited
    exited = True


def get_game_over() -> bool:
    global exited
    return exited


def set_fight_mode(mode: bool = True):
    global _fight_mode
    _fight_mode = mode


def get_fight_mode() -> bool:
    global _fight_mode
    return _fight_mode


def reset_turns():
    global turn
    turn = 0


def next_turn() -> int:
    global turn
    turn += 1
    return turn


def get_turn() -> int:
    global turn
    return turn


def get_player() -> Player:
    global _player
    return _player


def make_enemy(level: int | None = None) -> Entity:
    _l = int(level or get_player().level * 1.15) - 1
    _e = Entity(uuid4(),
                AttributeMap(),
                RaceInstance(Races.Human, Gender.Male),
                level=_l,
                skill_points=_l * 3 + 2)
    _e.set_name("Enemy")
    _e.add_level_listener(lambda _e: notify_level_up(_e))
    return _e


_enemy: Entity = make_enemy(1)


def get_enemy() -> Entity:
    global _enemy
    if _enemy.health <= 0:
        set_fight_mode(False)
        print("The enemy is dead! Generating a new one...")
        sleep(2)
        _enemy = make_enemy()
    return _enemy


def init_player():
    inform("Welcome to TBRPG, a turn-based fantasy RPG game.")
    sleep(1)
    inform("Let's now make your character!")
    sleep(2.5)
    print()

    inform("What is your name?")
    name = wait_for_string()
    get_player().set_name(name)
    sleep(0.4)
    inform("So, your name is {}? What an interesting name...".format(name))
    sleep(1)
    print()

    inform("What is your age?")
    age = wait_for_integer() or 18
    get_player().set_age(age)
    sleep(0.4)
    if age >= 30:
        inform("You're {}? You don't look a day over {}.".format(
            age, int(age * 0.70)))
    elif age >= 18:
        inform("{}? In the prime of adulthood.".format(age))
    else:
        inform("Only {}? Oh to be young...".format(age))
    sleep(1)
    print()

    ## wait_for_registered_item(Races.REGISTRY())
    inform("What is your race?")
    race = wait_for_string()
    get_player().set_race(Race.REGISTRY.get(race))
    
    """inform("What is your class?")
    cls = wait_for_string()
    get_player().set_class(Classes.REGISTRY()[cls])
    
    inform("What is your background?")
    bg = wait_for_string()
    get_player().set_background(bg)
    
    inform("What is your alignment?")
    align = wait_for_string()
    get_player().set_alignment(align)"""

    print()

    inform("One more step and you're all set to go, {}!".format(name))
    sleep(3)
    print()


def command_tutorial():
    inform("Let's dive into the command system.")
    sleep(1)
    inform("Each command performs a different action and may have parameters")
    inform("\tfor more specific results.")
    sleep(2.5)
    print()
    print()

    inform("The 'Status' command displays your status window.")
    sleep(1)
    inform("This lists all your core attributes, your experience, etc.")
    sleep(1)
    print()

    whisper(
        "\33[2mThe command also could specify exact sets of information to display."
    )
    whisper("\33[2mIt would then be used like 'Status [<section name>...]'")
    whisper("\33[2mEx: 'Status bars' shows the HP, MP, and STA amounts.")
    sleep(1.5)
    print()

    inform("The 'Invest [<attribute>] [<sp amount>]' command invests")
    inform("\tyour skill points in an attribute.")
    sleep(1)
    inform("'Invest' without parameters walks you through the process.")
    sleep(2.5)
    print()
