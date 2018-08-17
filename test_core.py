from core import *
from unittest import mock


def test_next_level_1():
    character = {'Player': {'Level': 10}}

    level = next_level(character)
    assert level == 1065


def test_next_level_2():
    character = {'Player': {'Level': 53}}

    level = next_level(character)

    assert level == 125971


def test_next_level_3():
    character = {'Player': {'Level': 100}}

    level = next_level(character)

    assert level == 0


@mock.patch('core.message_dialog')
def test_level_up_1(fake_prompt):
    fake_prompt.return_value = None
    character = {'Player': {'Level': 2, 'Exp': 21}}

    level_up(character)

    assert character['Player']['Level'] == 2
    assert character['Player']['Exp'] == 21


@mock.patch('core.message_dialog')
def test_level_up_2(fake_prompt):
    fake_prompt.return_value = None
    character = {'Player': {'Level': 99, 'Exp': 1624241}}

    level_up(character)

    assert character['Player']['Level'] == 100
    assert character['Player']['Exp'] == 824241


def test_level_up_3():
    character = {'Player': {'Level': 100, 'Exp': 824241}}

    level_up(character)

    assert character['Player']['Level'] == 100
    assert character['Player']['Exp'] == 0


def test_player_stats_1():
    character = {'Player': {'Name': 'John', 'Level': 10}}

    player = player_stats(character)

    assert player == {
        'Name': 'John',
        'Level': 10,
        'Max Health': 70,
        'Health': 70,
        'Mana': 30,
        'Damage_low': 7,
        'Damage_high': 13,
        'Evasion': 20
    }


def test_player_stats_2():
    character = {'Player': {'Name': 'John', 'Level': 52}}

    player = player_stats(character)

    assert player == {
        'Name': 'John',
        'Level': 52,
        'Max Health': 280,
        'Health': 280,
        'Mana': 114,
        'Damage_low': 28,
        'Damage_high': 44,
        'Evasion': 39
    }


def test_standard_mana_regen_1():
    player = {'Name': 'John', 'Level': 10, 'Mana': 24}

    player['Mana'] = standard_mana_regen(player)

    assert player['Mana'] == 29


def test_standard_mana_regen_2():
    player = {'Name': 'John', 'Level': 10, 'Mana': 29}

    player['Mana'] = standard_mana_regen(player)

    assert player['Mana'] == 30


def test_advance_mana_regen_1():
    player = {'Name': 'John', 'Level': 10, 'Mana': 19}

    player['Mana'] = advance_mana_regen(player)

    assert player['Mana'] == 29


def test_advance_mana_regen_2():
    player = {'Name': 'John', 'Level': 10, 'Mana': 25}

    player['Mana'] = advance_mana_regen(player)

    assert player['Mana'] == 30


@mock.patch('core.message_dialog')
@mock.patch('core.randint')
def test_attack_1(fake_num, fake_prompt):
    fake_num.side_effect = [14, 0]
    fake_prompt.return_value = None

    player = {
        'Name': 'John',
        'Level': 52,
        'Max Health': 280,
        'Health': 280,
        'Mana': 114,
        'Damage_low': 1,
        'Damage_high': 14,
        'Evasion': 39
    }

    bandit = {
        'Name': 'Lone Bandit',
        'Level': 1,
        'Max Health': 15,
        'Health': 15,
        'Max Mana': 5,
        'Mana': 5,
        'Damage_low': 2,
        'Damage_high': 5,
        'Evasion': 15,
        'Skill': 'Knife Throw'
    }

    attack(player, bandit)

    assert bandit['Health'] == 15


@mock.patch('core.message_dialog')
@mock.patch('core.randint')
def test_attack_2(fake_num, fake_prompt):
    fake_num.side_effect = [14, 25]
    fake_prompt.return_value = None

    player = {
        'Name': 'John',
        'Level': 52,
        'Max Health': 280,
        'Health': 280,
        'Mana': 114,
        'Damage_low': 1,
        'Damage_high': 14,
        'Evasion': 39
    }

    bandit = {
        'Name': 'Lone Bandit',
        'Level': 1,
        'Max Health': 15,
        'Health': 15,
        'Max Mana': 5,
        'Mana': 5,
        'Damage_low': 2,
        'Damage_high': 5,
        'Evasion': 15,
        'Skill': 'Knife Throw'
    }

    attack(player, bandit)

    assert bandit['Health'] == 1


@mock.patch('core.message_dialog')
@mock.patch('core.randint')
def test_attack_3(fake_num, fake_prompt):
    fake_num.side_effect = [16, 25]
    fake_prompt.return_value = None

    player = {
        'Name': 'John',
        'Level': 52,
        'Max Health': 280,
        'Health': 280,
        'Mana': 114,
        'Damage_low': 1,
        'Damage_high': 14,
        'Evasion': 39
    }

    bandit = {
        'Name': 'Lone Bandit',
        'Level': 1,
        'Max Health': 15,
        'Health': 15,
        'Max Mana': 5,
        'Mana': 5,
        'Damage_low': 2,
        'Damage_high': 5,
        'Evasion': 15,
        'Skill': 'Knife Throw'
    }

    attack(player, bandit)

    assert bandit['Health'] == 0


@mock.patch('core.message_dialog')
@mock.patch('core.randint')
def test_escape_1(fake_num, fake_prompt):
    fake_num.return_value = 50
    fake_prompt.return_value = None

    player = {'Name': 'John', 'Evasion': 39}

    bandit = {'Name': 'Lone Bandit', 'Evasion': 15}

    success = escape(player, bandit)

    assert success == 'Blocked'


@mock.patch('core.message_dialog')
@mock.patch('core.randint')
def test_escape_2(fake_num, fake_prompt):
    fake_num.return_value = 25
    fake_prompt.return_value = None

    player = {'Name': 'John', 'Evasion': 39}

    bandit = {'Name': 'Lone Bandit', 'Evasion': 15}

    success = escape(player, bandit)

    assert success == 'Escaped'


def test_prologue_enemy():
    bandit = prologue_enemy()

    assert bandit == {
        'Name': 'Lone Bandit',
        'Level': 1,
        'Max Health': 15,
        'Health': 15,
        'Max Mana': 5,
        'Mana': 5,
        'Damage_low': 2,
        'Damage_high': 5,
        'Evasion': 15,
        'Skill': 'Knife Throw'
    }


def test_forest_goblin():
    player = {'Level': 8}

    goblin = forest_goblin(player)

    assert goblin == {
        'Name': 'Slow Goblin',
        'Level': 7,
        'Max Health': 35,
        'Health': 35,
        'Max Mana': 10,
        'Mana': 10,
        'Damage_low': 3,
        'Damage_high': 8,
        'Evasion': 19,
        'Skill': 'Clobber'
    }


def test_forest_bandit():
    player = {'Level': 11}

    bandit = forest_bandit(player)

    assert bandit == {
        'Name': 'Bandit',
        'Level': 10,
        'Max Health': 50,
        'Health': 50,
        'Max Mana': 15,
        'Mana': 15,
        'Damage_low': 4,
        'Damage_high': 9,
        'Evasion': 25,
        'Skill': 'Knife Throw'
    }


@mock.patch('core.message_dialog')
def test_enemy_skill_1(fake_prompt):
    fake_prompt.return_value = None

    player = {'Health': 25}

    enemy = {'Name': 'Bandit', 'Level': 5, 'Mana': 5, 'Skill': 'Knife Throw'}

    enemy_skill(player, enemy)

    assert player['Health'] == 16
    assert enemy['Mana'] == 0


@mock.patch('core.message_dialog')
def test_enemy_skill_2(fake_prompt):
    fake_prompt.return_value = None

    player = {'Health': 5}

    enemy = {'Name': 'Bandit', 'Level': 5, 'Mana': 6, 'Skill': 'Knife Throw'}

    enemy_skill(player, enemy)

    assert player['Health'] == 0
    assert enemy['Mana'] == 1


def test_starved_wolf():
    player = {'Level': 6}

    wolf = starved_wolf(player)

    assert wolf == {
        'Name': 'Starved Wolf',
        'Level': 5,
        'Max Health': 25,
        'Health': 25,
        'Max Mana': 7,
        'Mana': 7,
        'Damage_low': 2,
        'Damage_high': 6,
        'Evasion': 15,
        'Heal': 'Lick Wounds'
    }


def test_bandit_leader():
    leader = bandit_leader()

    assert leader == {
        'Name': 'Bandit Leader',
        'Level': 10,
        'Max Health': 60,
        'Health': 60,
        'Max Mana': 20,
        'Mana': 20,
        'Damage_low': 5,
        'Damage_high': 11,
        'Evasion': 25,
        'Skill': 'Backstab',
        'Heal': 'Bandage',
        'Soul Power': 'Greed'
    }


@mock.patch('core.message_dialog')
def test_soul_power_1(fake_prompt):
    fake_prompt.return_value = None

    player = {'Name': 'John', 'Max Health': 50, 'Health': 45}

    enemy = {
        'Name': 'Boss',
        'Max Health': 50,
        'Health': 40,
        'Soul Power': 'Greed'
    }

    soul_power(player, enemy)

    assert player['Health'] == 40
    assert enemy['Health'] == 45


@mock.patch('core.message_dialog')
def test_soul_power_2(fake_prompt):
    fake_prompt.return_value = None

    player = {'Name': 'John', 'Max Health': 50, 'Health': 3}

    enemy = {
        'Name': 'Boss',
        'Max Health': 50,
        'Health': 47,
        'Soul Power': 'Greed'
    }

    soul_power(player, enemy)

    assert player['Health'] == 0
    assert enemy['Health'] == 50
