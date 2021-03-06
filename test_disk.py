from disk import *
from bcca.test import (
    should_print,
    fake_file,
)
from unittest import mock


@fake_file({'save.txt': '''header line
line
line
line
'''})
def test_save_read():
    save = 'save.txt'
    assert save_read(save) == 'line\nline\nline\n'


def test_save_to_character():
    contents = 'Matt,Sir,2,2100,300'

    content = save_to_character(contents)

    assert content == ('Matt', 'Sir', 2, 2100, 300)


@fake_file({'save.txt': '''header line
Matt,Sir,2,2100,300'''})
def test_load_save_1():
    save = 'save.txt'

    character = load_save(save)

    assert character == {
        'Player': {
            'Name': 'Matt',
            'Gender': 'Sir',
            'Level': 2,
            'Exp': 2100,
            'Gold': 300
        }
    }


@fake_file({'save.txt': '''headerline'''})
def test_load_save_2():
    save = 'save.txt'

    character = load_save(save)

    assert character == None


@fake_file({
    'inventory1.txt': '''header line
line
line
line''',
    'inventory2.txt': '''header line
line'''
})
def test_inventory_read_1():
    save = 'save1.txt'

    contents = inventory_read(save)

    assert contents == 'line\nline\nline'


@fake_file({
    'inventory1.txt': '''header line
line
line
line''',
    'inventory2.txt': '''header line
line'''
})
def test_inventory_read_2():
    save = 'save2.txt'

    contents = inventory_read(save)

    assert contents == 'line'


def test_inventory_to_bag():
    contents = '0,0,0,1'

    contents = inventory_to_bag(contents)

    assert contents == (0, 0, 0, 1)


@fake_file({
    'inventory1.txt': '''header line
0,0,1,0''',
    'inventory2.txt': '''header line
10,0,2,1'''
})
def test_load_inventory_1():
    save = 'save1.txt'

    bag = load_inventory(save)

    assert bag == {
        'Health Potion': 0,
        'Mana Potion': 0,
        'Elixir': 1,
        'Bomb': 0
    }


@fake_file({
    'inventory1.txt': '''header line
0,0,1,0''',
    'inventory2.txt': '''header line
10,0,2,1'''
})
def test_load_inventory_2():
    save = 'save2.txt'

    bag = load_inventory(save)

    assert bag == {
        'Health Potion': 10,
        'Mana Potion': 0,
        'Elixir': 2,
        'Bomb': 1
    }


@fake_file({
    'key_items1.txt': '''header
1,0,0''',
    'key_items2.txt': '''header
1,1,0'''
})
def test_key_items_read_1():
    save = 'save1.txt'

    contents = key_items_read(save)

    assert contents == ('1,0,0')


@fake_file({
    'key_items1.txt': '''header
1,0,0''',
    'key_items2.txt': '''header
1,1,0'''
})
def test_key_items_read_2():
    save = 'save2.txt'

    contents = key_items_read(save)

    assert contents == ('1,1,0')


def test_items_key():
    contents = '0'

    items_key(contents)

    assert contents == ('0')


@fake_file({
    'key_items1.txt': '''header
1''',
    'key_items2.txt': '''header
0'''
})
def test_load_keys_items_1():
    save = 'save1.txt'

    key_items = load_key_items(save)

    assert key_items == {'Bandit Leader\'s Dagger': True}


@fake_file({
    'key_items1.txt': '''header
1''',
    'key_items2.txt': '''header
0'''
})
def test_load_keys_items_2():
    save = 'save2.txt'

    key_items = load_key_items(save)

    assert key_items == {'Bandit Leader\'s Dagger': False}


def test_saving_game_1():
    character = {
        'Player': {
            'Name': 'John',
            'Gender': 'Sir',
            'Level': 10,
            'Exp': 143,
            'Gold': 563
        }
    }

    strings = saving_game(character)

    assert strings == 'name,gender,level,experience,gold\nJohn,Sir,10,143,563'


def test_saving_game_2():
    character = {
        'Player': {
            'Name': 'Jane',
            'Gender': 'Madam',
            'Level': 52,
            'Exp': 5234,
            'Gold': 2939
        }
    }

    strings = saving_game(character)

    assert strings == 'name,gender,level,experience,gold\nJane,Madam,52,5234,2939'


@mock.patch('disk.button_dialog')
@fake_file({
    'save1.txt': '''header''',
    'save2.txt': '''header\nJohn,Sir,52,5234,2939'''
})
def test_save_to_file_1(fake_prompt):
    fake_prompt.return_value = 'save1.txt'

    character = {
        'Player': {
            'Name': 'Jane',
            'Gender': 'Madam',
            'Level': 52,
            'Exp': 5234,
            'Gold': 2939
        }
    }

    save_to_file(character)

    assert save_to_file(character) == 'save1.txt'
    assert open('save1.txt').read() == '''name,gender,level,experience,gold
Jane,Madam,52,5234,2939'''


@mock.patch('disk.button_dialog')
@fake_file({
    'save1.txt': '''header''',
    'save2.txt': '''header\nJohn,Sir,53,100,239'''
})
def test_save_to_file_2(fake_prompt):
    fake_prompt.return_value = 'save2.txt'

    character = {
        'Player': {
            'Name': 'Jane',
            'Gender': 'Madam',
            'Level': 52,
            'Exp': 5234,
            'Gold': 2939
        }
    }

    save_to_file(character)

    assert save_to_file(character) == 'save2.txt'
    assert open('save2.txt').read() == '''name,gender,level,experience,gold
Jane,Madam,52,5234,2939'''


def test_saving_bag_1():
    bag = {'Health Potion': 1, 'Mana Potion': 3, 'Elixir': 2, 'Bomb': 5}

    inventory = saving_bag(bag)

    assert inventory == 'health potion,mana potion,elixir,bomb\n1,3,2,5'


def test_saving_bag_2():
    bag = {'Health Potion': 0, 'Mana Potion': 10, 'Elixir': 4, 'Bomb': 5}

    inventory = saving_bag(bag)

    assert inventory == 'health potion,mana potion,elixir,bomb\n0,10,4,5'


@fake_file({
    'inventory1.txt':
    '''health potion,mana potion,elixir,bomb
0,0,0,0''',
    'inventory2.txt':
    '''health potion,mana potion,elixir,bomb
0,10,4,5'''
})
def test_bag_to_inventory_1():
    bag = {'Health Potion': 1, 'Mana Potion': 3, 'Elixir': 2, 'Bomb': 5}

    save = 'save1.txt'

    bag_to_inventory(bag, save)

    assert open(
        'inventory1.txt').read() == '''health potion,mana potion,elixir,bomb
1,3,2,5'''


@fake_file({
    'inventory1.txt':
    '''health potion,mana potion,elixir,bomb
0,0,0,0''',
    'inventory2.txt':
    '''health potion,mana potion,elixir,bomb
0,10,4,5'''
})
def test_bag_to_inventory_2():
    bag = {'Health Potion': 2, 'Mana Potion': 0, 'Elixir': 1, 'Bomb': 10}

    save = 'save1.txt'

    bag_to_inventory(bag, save)

    assert open(
        'inventory1.txt').read() == '''health potion,mana potion,elixir,bomb
2,0,1,10'''


def test_saving_key_items_1():
    key_items = {'Bandit Leader\'s Dagger': True}

    items = saving_key_items(key_items)

    assert items == 'bandit dagger\n1'


def test_saving_key_items_2():
    key_items = {'Bandit Leader\'s Dagger': False}

    items = saving_key_items(key_items)

    assert items == 'bandit dagger\n0'


@fake_file({
    'key_items1.txt': 'bandit dagger\n0',
    'key_items2.txt': 'bandit dagger\n1'
})
def test_key_items_to_file_1():
    save = 'save1.txt'

    key_items = {'Bandit Leader\'s Dagger': True}

    key_items_to_file(key_items, save)

    assert open('key_items1.txt').read() == 'bandit dagger\n1'


@fake_file({
    'key_items1.txt': 'bandit dagger\n0',
    'key_items2.txt': 'bandit dagger\n1'
})
def test_key_items_to_file_2():
    save = 'save2.txt'

    key_items = {'Bandit Leader\'s Dagger': False}

    key_items_to_file(key_items, save)

    assert open('key_items1.txt').read() == 'bandit dagger\n0'
