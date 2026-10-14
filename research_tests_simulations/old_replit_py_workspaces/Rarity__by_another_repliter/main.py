# Imports

import replit, random, time
from getkey import getkey, keys
from research_tests_simulations.old_replit_py_workspaces.Rarity__by_another_repliter.randtext import text, items
from colorama import Fore, Style

# Hides Cursor

print('\033[?25l', end="")

# Establishes Variables

class person:
        def __init__(self, backpack, hp, max_hp, items):
                self.backpack = backpack
                self.hp = hp
                self.max_hp = max_hp
                self.items = items

Per = person(3, 20, 30, {})
        

class variables:
        def __init__(self, selection, selection_id, key, text, loops, wait, delete, event_name, swap_item, iteration, stored_var):
                self.selection = selection
                self.selection_id = selection_id
                self.key = key
                self.text = text
                self.loops = loops
                self.wait = wait
                self.delete = delete
                self.event_name = event_name
                self.swap_item = swap_item
                self.iteration = iteration
                self.stored_var = stored_var

Var = variables(["Start"], 0, '', 'Rarity', 3, 0.2, "", "", [], 0, "")

# Handles all events

def random_event(items, item_weights, item_choises):
        return random.choices(items, weights=item_weights, k=item_choises)

def random_choice(items, item_choises):
        return random.sample(items, item_choises)

def animation(loops, wait):
        d = '.'
        for i in range(loops):
                for i in range(3):
                        print(d)
                        d += '.'
                        time.sleep(wait)
                        replit.clear()
                d = '.'

def event(event_space):
        replit.clear()
        Var.selection = ["Continue"]
        if event_space == "Start":
                Var.text = "You wake up in a stone dungeon, you need to find a way out."
        elif event_space == "Inspect":
                if Var.event_name == "Give":
                        Var.loops = 1
                        weights = []
                        choices = []
                        for i in items:
                                weights.append(items[i][1])
                                choices.append(items[i])
                        item = random_event(choices, weights, 1)[0]
                        if len(Per.items) < Per.backpack:
                                Per.items[Var.iteration] = item
                                Var.iteration += 1
                                Var.text = f"You found a {item[0]}!"
                                Var.selection = ["Continue"]
                                Var.selection += ["Items"]
                        else:
                                Var.text = f"You found a {item[0]}, but your backpack is full..."
                                Var.swap_item = item
                                Var.delete = item[0]
                                Var.selection = ["Discard"]
                                Var.selection += ["Swap"]
        elif event_space == "Items":
                Var.text = f"{Fore.LIGHTBLUE_EX}Backpack: {len(Per.items)}/{Per.backpack}{Style.RESET_ALL}"
                e = 1
                for i in Per.items:
                        Var.selection += [f"{e}: {Per.items[i][0]}"]
                        e += 1
        elif Var.text == f"{Fore.LIGHTBLUE_EX}Backpack: {len(Per.items)}/{Per.backpack}{Style.RESET_ALL}" and event_space != "Continue":   
                for _, el in Per.items.items():
                    if event_space.split(': ')[1] in el:
                        varnameidklol = [x for x in el if x != event_space]
                        break
                desc = varnameidklol[3][0]
                Var.text = f'{event_space.split(": ")[1]}: "{desc}"'
                Var.delete = event_space.split(': ')[1]
                Var.stored_var = event_space.split(': ')[1]
                if varnameidklol[2] == "Food":
                        Var.selection += ["Use"]
                Var.selection += ["Delete"]
        elif event_space == "Delete":
                for _, el in Per.items.items():
                    if Var.delete in el:
                        varnameidklol = [x for x in el if x != event_space]
                        break
                key = list(filter(lambda x: Per.items[x] == varnameidklol, Per.items))[0]
                del Per.items[key]
                Var.text = f"{Var.delete} deleted."
        elif event_space == "Swap":
                Var.text = f"{Fore.RED}Pick an item to swap {Var.delete}{Fore.RED} with:{Style.RESET_ALL}"
                Var.selection = []
                e = 1
                for i in Per.items:
                        Var.selection += [f"{e}: {Per.items[i][0]}"]
                        e += 1
                Var.selection += [f"Discard {Var.delete}"]
        elif Var.text == f"{Fore.RED}Pick an item to swap {Var.delete}{Fore.RED} with:{Style.RESET_ALL}":
                for _, el in Per.items.items():
                    if event_space.split(': ')[1] in el:
                        varnameidklol = [x for x in el if x != event_space]
                        break
                key = list(filter(lambda x: Per.items[x] == varnameidklol, Per.items))[0]
                del Per.items[key]
                Per.items[key] = Var.swap_item
                Var.text = f"Swapped {varnameidklol[0]} for {Var.delete}."
        elif event_space == "Discard" or event_space == f"Discard {Var.delete}":
                Var.text = f"{Var.delete} discarded."
        elif event_space == "Use":
                for _, el in Per.items.items():
                    if Var.stored_var in el:
                        varnameidklol = [x for x in el if x != event_space]
                        break
                key = list(filter(lambda x: Per.items[x] == varnameidklol, Per.items))[0]
                if Per.items[key][2] == "Food":
                        if Per.hp != Per.max_hp:
                                health_diff = Per.max_hp - Per.hp
                                gained_health = Per.hp + Per.items[key][3][1]
                                health_gained = min(health_diff, gained_health)
                                Per.hp += Per.items[key][3][1]
                                Var.text = f"Healed {health_gained} hp."
                                if Per.hp > Per.max_hp:
                                        Per.hp = Per.max_hp
                                del Per.items[key]
                        else:
                               Var.text = "You're at full hp already." 
        elif event_space == "Stats":
                Var.text = f"Hp: {Per.hp}/{Per.max_hp}\nBackpack: {len(Per.items)}/{Per.backpack}"
        else:
                Var.event_name = ""
                Var.loops = 1
                weights = []
                choices = []
                for i in text:
                        weights.append(text[i][1])
                        choices.append(text[i][0])
                Var.text = random_event(choices, weights, 1)[0]
                id = choices.index(Var.text)
                if text[id][2] == "Give":
                        Var.selection += ["Inspect"]
                        Var.event_name = "Give"
                Var.selection += ["Items", "Stats"]
        replit.clear()
        Var.key = ''
        Var.selection_id = 0
        animation(Var.loops, Var.wait)
        menu()

# Menu / Text screen

def menu():
        print(Var.text)
        for i in Var.selection:
                if Var.selection_id == Var.selection.index(i):
                        print(f'> {i}')
                else:
                        print(i)
        if Var.key == '':
                input()
        else:
                event(Var.selection[Var.selection_id])

# Basic Input

def input():
        Var.key = getkey()
        if Var.key == keys.UP or Var.key == "w":
                if Var.selection_id - 1 >= 0:
                        Var.selection_id -= 1
                Var.key = ''
        elif Var.key == keys.DOWN or Var.key == "s":
                if Var.selection_id + 1 < len(Var.selection):
                        Var.selection_id += 1
                Var.key = ''
        elif Var.key == keys.ENTER:
                Var.selection_i = 0
        else:
                Var.key = ''
                input()
        replit.clear()
        menu()

menu()

#1234567890@#$%&!()*