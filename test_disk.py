from disk import *
from bcca.test import (
    should_print,
    fake_file,
)


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
