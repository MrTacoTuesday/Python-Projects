# Ok, so for the beta version of this game, I'm just going to have single sentence events. Options don't have any purpose except to move the game forward and items are unusable

from colorama import Fore, Style

# items = {"Basic": 100, "Common": 50, "Uncommon": 25, "Rare": 10, "Epic":5, "Legendary": 1, "Mythical": 0.1} - Probably going to use this to determine what you get. I'm also considering showing the player the chance of getting that specific rarities for items.

# [Text, Chance, type]

text = {
        0:[f"The lights {Fore.LIGHTYELLOW_EX}flicker{Style.RESET_ALL} a bit.", 50, "Normal"],
        1:[f"A {Fore.CYAN}chill{Style.RESET_ALL} runs down your spine.", 25, "Normal"],
        2:[f"A {Style.DIM}{Fore.LIGHTBLACK_EX}screech{Style.RESET_ALL} can be heard in the distance.", 10, "Normal"],
        3:[f"The walls here show signs of {Fore.BLUE}water damage.{Style.RESET_ALL}", 10, "Normal"],
        4:[f"A stain of {Fore.RED}blood{Style.RESET_ALL} is on the floor in front of you.", 5, "Normal"],
        5:[f"{Fore.LIGHTYELLOW_EX}You stumble upon a room with a table on it.{Style.RESET_ALL}", 1, "Give"],
        6:[f"The lights flickers as you walk by, casting {Fore.MAGENTA}shadows{Style.RESET_ALL} on the walls.", 50, "Normal"],
        7:[f"You hear the distant sound of {Fore.LIGHTCYAN_EX}dripping water{Style.RESET_ALL} echoing through the halls.", 25, "Normal"],
        8:[f"A faint {Style.DIM}{Fore.WHITE}breeze{Style.RESET_ALL} makes the air feel {Style.DIM}{Fore.BLUE}colder.{Style.RESET_ALL}", 25, "Normal"],
        9:[f"An {Style.DIM}{Fore.LIGHTBLACK_EX}echo{Style.RESET_ALL} can be heard in the distance", 10, "Normal"],
        10:[f"You smell the musty scent of {Style.DIM}{Fore.GREEN}mold{Style.RESET_ALL} and {Fore.LIGHTBLACK_EX}decay{Style.RESET_ALL}.", 25, "Normal"],
        11:[f"{Fore.LIGHTYELLOW_EX}You find a large chest in the middle of a dark room.{Style.RESET_ALL}", 1, "Give"],
        12:[f"{Fore.LIGHTYELLOW_EX}A fork in the path confronts you.{Style.RESET_ALL}", 1, "Options", ["Go Left", "Go Right", "Go forward"]],
        13:[f"An eerie {Fore.LIGHTBLACK_EX}silence{Style.RESET_ALL} weighs heavily on you.", 50, "Normal"],
        14:[f"{Style.DIM}{Fore.WHITE}The air grows thick, it makes it harder to breath.{Style.RESET_ALL}", 5, "Normal"],
        15:[f"The ground {Style.DIM}{Fore.RED}trembles{Style.RESET_ALL} beneath your feet...", 5, "Normal"],
        16:[f"A thin layer of {Fore.LIGHTBLACK_EX}fog{Style.RESET_ALL} obscures your vision.", 10, "Normal"],
        17:[f"{Style.DIM}{Fore.WHITE}Nothing here...{Style.RESET_ALL}", 250, "Normal"],
}

# [Item, Chance, type]

# Useless: Desc
# Food: Desc, Heal
# Weapn: Desc, Dmg

items = {
        0:[f"{Fore.LIGHTBLUE_EX}Water Bottle{Style.RESET_ALL}", 25, "Food", ["A standard bottle of water to quench your thirst. Heals 10 hp.", 10]],
        1:[f"{Fore.LIGHTYELLOW_EX}Bag of Chips{Style.RESET_ALL}", 10, "Food", ["A yellow bag of chips, pretty salty. Heals 25 hp.", 25]],
        2:[f"{Fore.LIGHTBLACK_EX}Metal Shard{Style.RESET_ALL}", 50, "Useless", ["A sharp metal shard, who knows where it came from..."]],
        3:[f"{Fore.CYAN}Ballpoint Pen{Style.RESET_ALL}", 50, "Useless", ["A standard ballpoint pen... It has blue ink."]],
        4:[f"{Fore.RED}Knife{Style.RESET_ALL}", 5, "Weapon", ["An old dull knife. Deals 10 dmg.", 10]],
}

#1234567890