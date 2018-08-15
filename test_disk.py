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
