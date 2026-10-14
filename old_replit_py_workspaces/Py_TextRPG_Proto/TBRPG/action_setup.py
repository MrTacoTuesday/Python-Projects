from random import random
from time import sleep

from ATTRIBUTE.attributes import Attributes
from ENTITY.entity import Entity

from .parse import (
    alert,
    inform,
    wait_for_command,
    wait_for_integer,
    wait_for_string,
    whisper,
)
from .world import (
    end_game,
    get_enemy,
    get_fight_mode,
    get_player,
    get_turn,
    next_turn,
    reset_turns,
    set_fight_mode,
)


def tryCommand():
    if get_fight_mode():
        if get_turn() % 2 == 1:
            action_Fight(get_enemy(), get_player())
        whisper("Your Move.")
    (cmd, *args) = wait_for_command()
    if cmd == "Status":
        # get sections from args
        action_Status(get_player())
    if cmd == "Peek":
        action_Status(get_enemy())
    if cmd == "Fight" and not get_fight_mode():
        action_Fight_engage()

    if get_fight_mode():
        if cmd == "Attack":
            action_Fight(get_player(), get_enemy())
        else:
            pass
    if cmd == "Invest":
        name, amount = None, None
        if len(args) >= 1:
            name = args[0]
        if len(args) >= 2:
            amount = int(args[1]) if args[1].isdigit() else None
        action_Invest(name, amount)
    if cmd == "/XP":
        amt = 0
        if len(args) >= 1:
            amt = int(args[0]) if args[0].isdigit() else 0
        get_player().gain_experience(amt)
    if cmd == "/PLAYER":
        arg = " ".join(args)
        try:
            e = eval("get_player().{}".format(arg))
            if e is not None:
                whisper(e)
        except Exception:
            pass
    if cmd == "/ENEMY":
        arg = " ".join(args)
        try:
            e = eval("get_enemy().{}".format(arg))
            if e is not None:
                whisper(e)
        except Exception:
            pass
    if cmd == "Quit":
        alert("Are You Sure? (Y/n)")
        if wait_for_string() == "Y":
            alert("Exiting Game...")
            sleep(3)
            inform("Thanks for playing!")
            end_game()


def action_Status(entity: Entity):
    entity.printStatusWindow()


def action_Fight_engage():
    set_fight_mode()
    whisper("You engage in combat!")
    print()
    sleep(2)
    reset_turns()
    if random() < 0.5:
        next_turn()


def action_Fight(source: Entity, target: Entity):
    print("{} attacks with their fists!".format(source.name))
    sleep(0.6)
    dmg, crit = source.try_attack(target)
    if crit:
        print(f"Critical hit! {target.name} took {dmg:.1f} damage.")
    else:
        print(f"{source.name} dealt {dmg:.1f} damage to {target.name}.")
    print()
    sleep(0.8)
    target.harm(dmg, source)
    if target.health <= 0:
        print(f"{target.name} has been defeated!")
        print(f"{source.name} gains {target.experience_dropped} XP.")
        print()
        sleep(0.6)
        set_fight_mode(False)
        action_Status(get_enemy())
        return
    next_turn()


def action_Invest(attr_name: str | None = None, sp_amount: int | None = None):
    valid = {
        attr.name
        for attr in Attributes.REGISTRY().values() if attr.investable
    }
    if attr_name is None:
        inform("What Attribute would you like to invest into?")
    cmd = attr_name or wait_for_string()
    while cmd not in valid:
        alert("Invalid Attribute Name")
        whisper("Valid Attributes are: {}".format(", ".join(sorted(valid))))
        print()
        inform("What Attribute would you like to invest into?")
        cmd = wait_for_string()
    attr = Attributes.REGISTRY()[cmd]
    if sp_amount is None:
        inform(
            "How much SP would you like to invest into {}? \33[3m(You currently have {})"
            .format(attr.name,
                    get_player().skill_points))
    sp = sp_amount or wait_for_integer()
    while sp is None or sp > get_player().skill_points:
        alert("Invalid SP Amount")
        print()
        inform(
            "How much SP would you like to invest into {}? \33[3m(You currently have {})"
            .format(attr.name,
                    get_player().skill_points))
        sp = wait_for_integer()
    get_player().invest_sp(attr, sp)
    print("Invested {} SP into {}".format(sp, attr.name))
    print()


# def action_Inventory

# def action_Equip

# def action_Unequip

# def action_Skills

# def action_Save

####
