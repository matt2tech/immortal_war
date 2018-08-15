from prompt_toolkit.shortcuts import *

# Loading save


# reads a save from one of the three save slots; each save slot
# is a separate save.txt file
def save_read(save):
    with open(save, 'r') as file:
        file.readline()
        contents = file.read()
    return contents


# converts the file data to character data
def save_to_character(contents):
    stats = contents.split(',')
    return stats[0], stats[1], int(stats[2]), int(stats[3]), int(stats[4])


# using save_read and save_to_character to create character stats,
# this will load up a save if there is one
def load_save(save):
    contents = save_read(save)
    if contents == '':
        return None
    else:
        lines = contents.split('\n')
        for line in lines:
            if line:
                stats = save_to_character(line)
                character = {
                    'Player': {
                        'Name': stats[0],
                        'Gender': stats[1],
                        'Level': stats[2],
                        'Exp': stats[3],
                        'Gold': stats[4]
                    }
                }

        return character


# reads the inventory data saved on inventory.txt
def inventory_read(save):
    if save == 'save1.txt':
        with open('inventory1.txt', 'r') as file:
            file.readline()
            contents = file.read()
        return contents
    elif save == 'save2.txt':
        with open('inventory2.txt', 'r') as file:
            file.readline()
            contents = file.read()
        return contents
    if save == 'save3.txt':
        with open('inventory3.txt', 'r') as file:
            file.readline()
            contents = file.read()
        return contents


# converts the inventory data to bag data
def inventory_to_bag(contents):
    items = contents.split(',')
    return int(items[0]), int(items[1]), int(items[2]), int(items[3])


# using inventory_read and inventory_to_bag to create the bag,
# this will load up inventory associated with a save and creates
# items for the player's bag from the inventory
def load_inventory(save):
    contents = inventory_read(save)
    lines = contents.split('\n')
    for line in lines:
        if line:
            items = inventory_to_bag(line)
            bag = {
                'Health Potion': items[0],
                'Mana Potion': items[1],
                'Elixir': items[2],
                'Bomb': items[3]
            }

    return bag


def key_items_read(save):
    if save == 'save1.txt':
        with open('key_items1.txt', 'r') as file:
            file.readline()
            contents = file.read()
        return contents
    elif save == 'save2.txt':
        with open('key_items2.txt', 'r') as file:
            file.readline()
            contents = file.read()
        return contents
    elif save == 'save3.txt':
        with open('key_items3.txt', 'r') as file:
            file.readline()
            contents = file.read()
        return contents


# make sure to add to key items as game is built
def items_key(contents):
    items = contents.split(',')
    return (items[0])


def load_key_items(save):
    contents = key_items_read(save)
    lines = contents.split('\n')
    for line in lines:
        if line:
            items = items_key(line)
            key_items = {'Bandit Leader\'s Dagger': bool(int(items[0]))}
    return key_items


# Saving game


def saving_game(character):
    strings = []
    for stats, info in character.items():
        name = info['Name']
        gender = info['Gender']
        lvl = info['Level']
        exp = info['Exp']
        gold = info['Gold']
        string = '{},{},{},{},{}'.format(name, gender, lvl, exp, gold)
        strings.append(string)
        strings.sort()
        character = '{},{},{},{},{}\n{}'.format('name', 'gender', 'level',
                                                'experience', 'gold',
                                                '\n'.join(strings))
        return character


def save_to_file(character):
    save = saving_game(character)
    text = button_dialog(
        title='Load',
        text='',
        buttons=[('Save 1', 'save1.txt'), ('Save 2', 'save2.txt'),
                 ('Save 3', 'save3.txt')])
    with open(text, 'w') as file:
        file.write(save)
        return text


def saving_bag(bag):
    strings = []
    health = bag['Health Potion']
    mana = bag['Mana Potion']
    elixir = bag['Elixir']
    bomb = bag['Bomb']
    string = '{},{},{},{}'.format(health, mana, elixir, bomb)
    strings.append(string)
    strings.sort()
    bag = '{},{},{},{}\n{}'.format('health potion', 'mana potion', 'elixir',
                                   'bomb', '\n'.join(strings))
    return bag


def bag_to_inventory(bag, save):
    if save == 'save1.txt':
        text = saving_bag(bag)
        with open('inventory1.txt', 'w') as file:
            file.write(text)
    elif save == 'save2.txt':
        text = saving_bag(bag)
        with open('inventory2.txt', 'w') as file:
            file.write(text)
    elif save == 'save3.txt':
        text = saving_bag(bag)
        with open('inventory3.txt', 'w') as file:
            file.write(text)


def saving_key_items(key_items):
    strings = []
    bandit_sword = int(key_items['Bandit Leader\'s Dagger'])
    string = '{}'.format(bandit_sword)
    strings.append(string)
    strings.sort()
    key_items = '{}\n{}'.format('bandit dagger', '\n'.join(strings))
    return key_items


def key_items_to_file(key_items, save):
    if save == 'save1.txt':
        text = saving_key_items(key_items)
        with open('key_items1.txt', 'w') as file:
            file.write(text)
    elif save == 'save2.txt':
        text = saving_key_items(key_items)
        with open('key_items2.txt', 'w') as file:
            file.write(text)
    elif save == 'save3.txt':
        text = saving_key_items(key_items)
        with open('key_items3.txt', 'w') as file:
            file.write(text)
