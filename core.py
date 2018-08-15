from random import randint
from math import ceil
from time import sleep
from prompt_toolkit.shortcuts import *

# core will deal mostly with battle functions

# Note: all normal enemies', maybe scripted enemies, stats should be universal to enemy_ai and vice versa
# as that is their ai. bosses' stats should be universal to boss_ai and vice versa


# helps with leveling up system. gives how much exp is needed for the next level
def next_level(character):
    return round((4 * ((character['Player']['Level'] + 1)**3)) / 5)


# levels up the player once they reached a certain threshold
def level_up(character):
    lvl_up = next_level(character)
    while character['Player']['Exp'] >= lvl_up:
        character['Player']['Exp'] = character['Player']['Exp'] - lvl_up
        character['Player']['Level'] += 1
        lvl_up = next_level(character)
        text = message_dialog(
            title='Level Up',
            text='You have reached new heights. You\'re level {} now'.format(
                character['Player']['Level']))
        if character['Player']['Level'] == 25:
            text = message_dialog(
                title='Level Up',
                text=
                'The Hero Soul within you imparts the skill Heal to you\nHeal will recover one-fourth of your health'
            )


# this function will be used to create stats for the player in battle
# (correlates with other battle related functions and enemy stat functions are used for enemies)
def player_stats(character):
    lvl = character['Player']['Level']
    player = {
        'Name': character['Player']['Name'],
        'Level': lvl,
        'Max Health': 20 + 5 * lvl,
        'Health': 20 + 5 * lvl,
        'Mana': 10 + 2 * lvl,
        'Damage_low': 2 + ceil(0.5 * lvl),
        'Damage_high': 5 + ceil(0.75 * lvl),
        'Evasion': 15 + ceil(0.45 * lvl)
    }
    return player


# regens mana for most actions during aside from wait and skills
def standard_mana_regen(friend):
    total = 10 + 2 * friend['Level']
    regen = min(total, friend['Mana'] + total // 6)
    return regen


# used with wait action. regens more mana than standard_mana_regen
def advance_mana_regen(friend):
    total = 10 + 2 * friend['Level']
    regen = min(total, friend['Mana'] + total // 3)
    return regen


# used with attack action. friend deals dmg to foe health
def attack(friend, foe):
    attack = randint(friend['Damage_low'], friend['Damage_high'])
    accuracy = randint(1, 100)
    if accuracy > foe['Evasion']:
        foe['Health'] = max(foe['Health'] - attack, 0)
        text = message_dialog(
            title='Battle',
            text='{} attacked {} dealing {} DMG'.format(
                friend['Name'], foe['Name'], attack))

    else:
        text = message_dialog(
            title='Battle', text='{} missed'.format(friend['Name']))


# used run action. player will use a turn to take a chance to escape from the battle
def escape(player, enemy):
    escape = randint(1, 100)
    if escape > player['Evasion']:
        text = message_dialog(
            title='Battle', text='{} blocks your escape'.format(enemy['Name']))
        return 'Blocked'
    else:
        text = message_dialog(
            title='Battle', text='{} escaped'.format(player['Name']))
        sleep(1)
        return 'Escaped'


# the first enemy in the game. Easiest (should be easiest) and used to explain how to battle to the player
def prologue_enemy():
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
    return bandit


# stats for goblin in forest dungeon. all enemies' stats, aside from bosses and scripted enemies,
# should be scaled to enemy's lvl and that should be scaled to player's lvl
# this enemy's max lvl should stay at or under lvl 10
def forest_goblin(player):
    lvl = min(max(randint(player['Level'] - 1, player['Level'] + 1), 1), 7)
    goblin = {
        'Name': 'Slow Goblin',
        'Level': lvl,
        'Max Health': 7 + 4 * lvl,
        'Health': 7 + 4 * lvl,
        'Max Mana': 3 + 1 * lvl,
        'Mana': 3 + 1 * lvl,
        'Damage_low': 1 + ceil(lvl * 0.2),
        'Damage_high': 4 + ceil(lvl * 0.5),
        'Evasion': 12 + lvl,
        'Skill': 'Clobber'
    }
    return goblin


# stats for bandit in forest dungeon. this enemy's max lvl should stay at or under lvl 10
def forest_bandit(player):
    lvl = min(max(randint(player['Level'] - 1, player['Level'] + 1), 1), 10)
    bandit = {
        'Name': 'Bandit',
        'Level': lvl,
        'Max Health': 10 + 4 * lvl,
        'Health': 10 + 4 * lvl,
        'Max Mana': 5 + 1 * lvl,
        'Mana': 5 + 1 * lvl,
        'Damage_low': 2 + ceil(lvl * 0.2),
        'Damage_high': 4 + ceil(lvl * 0.5),
        'Evasion': 15 + lvl,
        'Skill': 'Knife Throw'
    }
    return bandit


# the ai for normal enemies during battles. should be used for all normal battles and maybe scripted battles
# normal enemies have two moves, attack and skill. this ai deals with only those moves and it should be universal
# to all normal enemies
def enemy_ai(player, enemy):
    if enemy['Mana'] >= 5:
        if 'Skill' in enemy and player['Health'] > enemy['Health']:
            skill = 4 + enemy['Level']
            text = message_dialog(
                title='Battle',
                text='{} used {} dealing {} DMG'.format(
                    enemy['Name'], enemy['Skill'], skill))
            player['Health'] = max(player['Health'] - skill, 0)
            enemy['Mana'] -= 5
        elif 'Heal' in enemy and enemy['Health'] <= enemy['Max Health'] / 2:
            heal = randint(enemy['Level'], enemy['Level'] + 5)
            text = message_dialog(
                title='Battle',
                text='{} used {} and recovered {} Health'.format(
                    enemy['Name'], enemy['Heal'], enemy['Level']))
            enemy['Health'] = min(heal + enemy['Health'], enemy['Max Health'])
            enemy['Mana'] -= 5
    else:
        attack(enemy, player)
        mana = enemy['Max Mana']
        enemy['Mana'] = min(mana,
                            max(enemy['Mana'] + mana // 6, enemy['Mana'] + 1))


# stats for wolf in forest dungeon. this enemy's max lvl should stay at or under lvl 10
def starved_wolf(player):
    lvl = min(max(randint(player['Level'] - 1, player['Level'] + 1), 1), 5)
    wolf = {
        'Name': 'Starved Wolf',
        'Level': lvl,
        'Max Health': 5 + 4 * lvl,
        'Health': 5 + 4 * lvl,
        'Max Mana': 2 + 1 * lvl,
        'Mana': 2 + 1 * lvl,
        'Damage_low': 1 + ceil(lvl * 0.2),
        'Damage_high': 3 + ceil(lvl * 0.5),
        'Evasion': 10 + lvl,
        'Heal': 'Lick Wounds'
    }
    return wolf


# stats for the boss in forest dungeon. this enemy's lvl should stay at lvl 10
# stats are not scaled to player's lvl. if needed they can be scaled to enemy's lvl
def bandit_leader():
    leader = {
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
    return leader


# ai for bosses in battles. bosses have more moves than regular enemies
# this ai accounts for bosses stronger stats and additional moves
def boss_ai(player, enemy):
    if enemy['Mana'] >= 10 and enemy['Health'] <= enemy['Max Health'] * 0.75:
        heal = randint(enemy['Level'], enemy['Level'] + 5)
        text = message_dialog(
            title='Battle',
            text='{} used {} and recovered {} Health'.format(
                enemy['Name'], enemy['Heal'], enemy['Level']))
        enemy['Health'] = min(heal + enemy['Health'], enemy['Max Health'])
        enemy['Mana'] -= 10
    elif enemy['Mana'] >= 10 and player['Health'] > enemy['Health']:
        skill = enemy['Level'] * 1.5
        player['Health'] = max(player['Health'] - skill, 0)
        enemy['Mana'] -= 10
        text = message_dialog(
            title='Battle',
            text='{} used {} dealing {} DMG'.format(enemy['Name'],
                                                    enemy['Skill'], skill))
    else:
        attack(enemy, player)
        mana = enemy['Max Mana']
        enemy['Mana'] = min(mana,
                            max(enemy['Mana'] + mana // 6, enemy['Mana'] + 1))


# most bosses will have their own unique soul power
def soul_power(player, enemy):
    # the greed soul is the bandit leader's soul power
    if enemy['Soul Power'] == 'Greed':
        player['Health'] = max(player['Health'] - 5, 0)
        enemy['Health'] = min(enemy['Max Health'], enemy['Health'] + 5)
        text = message_dialog(
            title='The Greed Soul',
            text='{} absorbed Health from {}'.format(enemy['Name'],
                                                     player['Name']))
