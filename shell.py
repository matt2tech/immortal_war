from time import sleep
from disk import *
from core import *
from random import choice, randint
# from mob_images import *
from text_images import *
from prompt_toolkit.shortcuts import *
import sys
from os import system, name


def loads():
    text = button_dialog(
        title='Load',
        text='',
        buttons=[('Save 1', 'save1.txt'), ('Save 2', 'save2.txt'),
                 ('Save 3', 'save3.txt')])
    return text


# just a clear screen function
def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# after every battle the character stats need to be reloaded so the player's level updates properly
def player_reload(character):
    level_up(character)
    player = {
        'Player': {
            'Name': character['Player']['Name'],
            'Gender': character['Player']['Gender'],
            'Level': character['Player']['Level'],
            'Exp': character['Player']['Exp'],
            'Gold': character['Player']['Gold']
        }
    }
    return player


# title screen. players will be able to start a new game or load an old one
def start_menu():
    title()
    option = input('{:<37}{:>37}\n>>> '.format('1 - New Game',
                                               '2 - Load Game'))
    if option == '1':
        game = 'New'
        return game
    elif option == '2':
        game = 'Load'
        return game
    else:
        main()


# this sets the gender of the player
def gender_class():
    result = button_dialog(
        title='Prologue',
        text='Are you male or female?',
        buttons=[('Male', 'Sir'), ('Female', 'Madam')],
    )
    if result == None:
        gender_class()
    else:
        return result


# this sets the name of the player
def naming():
    text = input_dialog(title='Prologue', text='What is your name?').strip()
    if text == None or text == '':
        naming()
    else:
        return text


# asks where the player came from and depending on where, players start with preset gold and exp
def origin_story():
    result = button_dialog(
        title='Prologue',
        text='Where were you born?',
        buttons=[('City', 'Rich'), ('Farm', 'Decent'), ('Slums', 'Poor')],
    )
    if result == 'Rich':
        text = message_dialog(
            title='Prologue',
            text="""Being the child of upper-class parents, you enjoyed
the luxuries money brought. You have plenty of money
to begin your journey; however, being protected most
of your life, you lack experience.""")
        return result
    elif result == 'Decent':
        text = message_dialog(
            title='Prologue',
            text="""Being the child of middle-class parents, you had
everything you needed and some. You have some
money and experience to begin your journey.""")
        return result
    elif result == 'Poor':
        story = 'Being the child of lower-class parents, you had\nto work and struggle to survive. You have no money\nto begin your journey; however, having to struggle\nmost of your life, you have plenty of experience.'
        text = message_dialog(title='Prologue', text='{:-^50}'.format(story))
        return result


# allows player to view their stats and items in inventory
def character_menu(character, bag):
    menus = button_dialog(
        title='Journal',
        text='',
        buttons=[('Stats', '1'), ('Bag', '2'), ('Close Book', None)])
    if menus == '1':
        text = message_dialog(
            title='Stats',
            text='Name: {}\nGender: {}\nLevel: {}\nExp Needed: {}\nGold: {}'.
            format(character['Player']['Name'], character['Player']['Gender'],
                   character['Player']['Level'],
                   next_level(character) - character['Player']['Exp'],
                   character['Player']['Gold']))
        character_menu(character, bag)
    elif menus == '2':
        text = message_dialog(
            title='Bag',
            text='Health Potions: {}\nMana Potions: {}\nElixirs: {}\nBombs: {}'.
            format(bag['Health Potion'], bag['Mana Potion'], bag['Elixir'],
                   bag['Bomb']))
        character_menu(character, bag)


# asks the player what they would like to use their turn in battle for
# and returns the choice
def player_turn(player, enemy):
    player_lvl = player['Level']
    player_hp = player['Health']
    player_mp = player['Mana']
    enemy_lvl = enemy['Level']
    enemy_hp = enemy['Health']
    enemy_mp = enemy['Mana']
    result = button_dialog(
        title='Battle',
        text='{:^130}\n{:^130}'.format(
            'Level {} {} || {} HP {} MP'.format(player_lvl, player['Name'],
                                                player_hp, player_mp),
            'Level {} {} || {} HP {} MP'.format(enemy_lvl, enemy['Name'],
                                                enemy_hp, enemy_mp)),
        buttons=[('Attack', '1'), ('Spells', '2'), ('Items', '3'),
                 ('Wait', '4'), ('Run', '5')],
    )
    return result


# opens if the player chooses Items button in player_turn
# asks the player which item they would like to use and applies the effects of the item
# item used will be deducted one from the item key value from inventory dictionary
def items(bag, player, enemy):
    result = button_dialog(
        title='Items',
        text='',
        buttons=[('HP Potion', '2'), ('MP Potion', '3'), ('Elixir', '4'),
                 ('Bomb', '5'), ('Cancel', '1')],
    )
    if result == '1':
        return '1'
    elif result == '2':
        if bag['Health Potion'] > 0:
            text = message_dialog(
                title='Battle', text='1 HP Potion used\nHP recovered')
            player['Health'] = min(player['Max Health'],
                                   player['Max Health'] // 2)
            bag['Health Potion'] -= 1
        else:
            text = message_dialog(title='Battle', text='No HP Potions')
            return '1'
    elif result == '3':
        if bag['Mana Potion'] > 0:
            text = message_dialog(
                title='Battle', text='1 MP Potion used\nMP recovered')
            player['Mana'] = 10 + 2 * player['Level']
            bag['Mana Potion'] -= 1
        else:
            text = message_dialog(title='Battle', text='No MP Potions')
            return '1'
    elif result == '4':
        if bag['Elixir'] > 0:
            text = message_dialog(
                title='Battle', text='1 Elixir used\nHP and MP recovered')
            player['Health'] = 20 + 5 * player['Level']
            player['Mana'] = 10 + 2 * player['Level']
            bag['Elixir'] -= 1
        else:
            text = message_dialog(title='Battle', text='No Elixirs')
            return '1'
    elif result == '5':
        if bag['Bomb'] > 0:
            text = message_dialog(title='Battle', text='1 Bomb thrown')
            dmg = 3 * randint(player['Damage_low'], player['Damage_high'])
            enemy['Health'] = max(enemy['Health'] - dmg, 0)
            bag['Bomb'] -= 1
            print('{} blew up {} dealing {} DMG'.format(
                player['Name'], enemy['Name'], dmg))
        else:
            text = message_dialog(title='Battle', text='No Bombs')
            return '1'


# battle function for scripted enemies the player can not run from these
# battles wins in these battles yield slightly more exp and gold than normal battles
def scripted_battle(player, enemy, character, bag):
    while True:
        combat_choice = player_turn(player, enemy)
        if combat_choice == '1':
            attack(player, enemy)
            player['Mana'] = standard_mana_regen(player)
        elif combat_choice == '2':
            spell = spells(player, enemy)
            if spell == '5':
                continue
        elif combat_choice == '3':
            item = items(bag, player, enemy)
            if item == '1':
                continue
            else:
                player['Mana'] = standard_mana_regen(player)
        elif combat_choice == '4':
            print('You wait')
            player['Mana'] = advance_mana_regen(player)
        elif combat_choice == '5':
            text = message_dialog(
                title='Battle',
                text='{} blocks your escape'.format(enemy['Name']))
            player['Mana'] = standard_mana_regen(player)
        if enemy['Health'] == 0:
            exp = int(enemy['Level']**2)
            gold = randint(50, 100)
            text = message_dialog(
                title='Victory',
                text='{} has fallen\n{} gained {} EXP\n{} found {} Gold'.
                format(enemy['Name'], player['Name'], exp, player['Name'],
                       gold))
            character['Player']['Exp'] += exp
            character['Player']['Gold'] += gold
            break
        enemy_ai(player, enemy)
        if player['Health'] == 0:
            text = message_dialog(
                title='Defeat', text='You have fallen\nGAME OVER\n')
            main()


# battle function for normal enemies. players can run from these unlike scripted and boss battles
# yield between 20-25 gold and level scaled exp
def battle(player, enemy, character, bag):
    while True:
        combat_choice = player_turn(player, enemy)
        if combat_choice == '1':
            attack(player, enemy)
            player['Mana'] = standard_mana_regen(player)
        elif combat_choice == '2':
            spell = spells(player, enemy)
            if spell == '5':
                continue
        elif combat_choice == '3':
            item = items(bag, player, enemy)
            if item == '1':
                continue
            else:
                player['Mana'] = standard_mana_regen(player)
        elif combat_choice == '4':
            print('You wait')
            player['Mana'] = advance_mana_regen(player)
        elif combat_choice == '5':
            success = escape(player, enemy)
            if success == 'Escaped':
                break
            elif success != 'Escaped':
                player['Mana'] = standard_mana_regen(player)
        if enemy['Health'] == 0:
            exp = int(enemy['Level']**2)
            gold = randint(20, 25)
            text = message_dialog(
                title='Victory',
                text='{} has fallen\n{} gained {} EXP\n{} found {} Gold'.
                format(enemy['Name'], player['Name'], exp, player['Name'],
                       gold))
            character['Player']['Exp'] += exp
            character['Player']['Gold'] += gold
            break
        enemy_ai(player, enemy)
        if player['Health'] == 0:
            text = message_dialog(
                title='Defeat', text='You have fallen\nGAME OVER\n')
            main()


# battle function for bosses. players can not run from these
# yield the most exp and gold
def boss_battle(player, enemy, character, bag):
    while True:
        combat_choice = player_turn(player, enemy)
        if combat_choice == '1':
            attack(player, enemy)
            player['Mana'] = standard_mana_regen(player)
        elif combat_choice == '2':
            spell = spells(player, enemy)
            if spell == '5':
                continue
        elif combat_choice == '3':
            item = items(bag, player, enemy)
            if item == '1':
                continue
            else:
                player['Mana'] = standard_mana_regen(player)
        elif combat_choice == '4':
            print('You wait')
            player['Mana'] = advance_mana_regen(player)
        elif combat_choice == '5':
            print('{} blocks your escape'.format(enemy['Name']))
            player['Mana'] = standard_mana_regen(player)
        if enemy['Health'] == 0:
            exp = int(enemy['Level']**2.5)
            gold = randint(50, 100)
            text = message_dialog(
                title='Victory',
                text='{} has fallen\n{} gained {} EXP\n{} found {} Gold'.
                format(enemy['Name'], player['Name'], exp, player['Name'],
                       gold))
            character['Player']['Exp'] += exp
            character['Player']['Gold'] += gold
            break
        boss_ai(player, enemy)
        soul_power(player, enemy)
        if player['Health'] == 0:
            text = message_dialog(
                title='Defeat', text='You have fallen\nGAME OVER\n')
            main()


# shop interface for players to purchase items for battle
# purchases add to the item purchased key value in inventory dictionary
def shop(bag, character):
    buy = ''
    while buy != '1':
        buy = input(
            '\nYou enter the shop\nWhat would you like to buy?\nGold: {}\n1 - Leave\n2 - Health Potion || 250 Gold\n3 - Mana Potion || 250 Gold\n4 - Elixir || 1000 Gold\n5 - Bomb || 500 Gold\n>>> '.
            format(character['Player']['Gold']))
        if buy == '1':
            print('You leave the store')
        elif buy == '2':
            if character['Player']['Gold'] >= 250:
                bag['Health Potion'] += 1
                character['Player']['Gold'] -= 250
                print('1 Health Potion bought')
            else:
                print('Not enough Gold')
        elif buy == '3':
            if character['Player']['Gold'] >= 250:
                bag['Mana Potion'] += 1
                character['Player']['Gold'] -= 250
                print('1 Mana Potion bought')
            else:
                print('Not enough Gold')
        elif buy == '4':
            if character['Player']['Gold'] >= 1000:
                bag['Elixir'] += 1
                character['Player']['Gold'] -= 1000
                print('1 Elixir bought')
            else:
                print('Not enough Gold')
        elif buy == '5':
            if character['Player']['Gold'] >= 500:
                bag['Bomb'] += 1
                character['Player']['Gold'] -= 500
                print('1 Bomb bought')
            else:
                print('Not enough Gold')
        else:
            print('Choose a valid option')


def trainer(character):
    if character['Player']['Level'] >= 10:
        print('TRAINING MONTAGE')
    else:
        print('Come back when youre stronger')


def spells(player, enemy):
    if player['Level'] <= 24:
        text = button_dialog(
            title='Spells', text='', buttons=[('Flare', '1'), ('Cancel', '5')])
    elif player['Level'] <= 49:
        text = button_dialog(
            title='Spells',
            text='',
            buttons=[('Flare', '1'), ('Heal', '2'), ('Cancel', '5')])
    if text == '1':
        if player['Mana'] >= 10 + ceil(0.25 * player['Level']):
            dmg = randint(2 + ceil(0.5 * player['Level']),
                          4 + ceil(0.75 * player['Level']))
            enemy['Max Health'] = max(enemy['Max Health'] - dmg, 0)
            enemy['Health'] = max(enemy['Health'] - dmg, 0)
            player['Mana'] -= 10 + ceil(0.25 * player['Level'])
            text = message_dialog(
                title='Battle',
                text='{} burned {} dealing {} of Burn DMG'.format(
                    player['Name'], enemy['Name'], dmg))
        else:
            text = message_dialog(title='Battle', text='Need more mana')
            return '5'
    elif text == '5':
        return '5'


# runs the program
def main():
    clear()
    system('setterm -cursor off')
    game = start_menu()
    if game == 'New':
        name = naming()
        gender = gender_class()
        origin = origin_story()
        if origin == 'Rich':
            gold = 500
            lvl = 1
        elif origin == 'Decent':
            gold = 250
            lvl = 2
        elif origin == 'Poor':
            gold = 0
            lvl = 3
        character = {
            'Player': {
                'Name': name,
                'Gender': gender,
                'Level': lvl,
                'Exp': 0,
                'Gold': gold,
                'Weapon': None
            }
        }
        bag = {'Health Potion': 0, 'Mana Potion': 0, 'Elixir': 0, 'Bomb': 0}
        key_items = {'Bandit Leader\'s Dagger': False}
        clear()
        system('setterm -cursor off')
        print('\nLoading...\n{} {}\tLevel: {} - Gold: {}\n'.format(
            character['Player']['Gender'], character['Player']['Name'],
            character['Player']['Level'], character['Player']['Gold']))
        loading()
        text = message_dialog(
            title='Prologue',
            text="""Today is the day. You have reached the age of
adulthood and now are ready to go forth into life
by yourself. You have said your goodbyes to your
family. You leave your childhood home behind you
as you journey forth towards the capital.""")
        text = message_dialog(
            title='Prologue',
            text='''Your journey takes several days with no problems.
However, on the third day, you're walking along
the road at a steady pace when you notice a
broken down wagon. As you get closer, a fairly
husky man struggling to repair the wagon. The
man looks up and notices you.''')
        text = message_dialog(
            title='Prologue',
            text='''Before the man can say anything, you are
are ambushed by bandits. The bandits rush
towards the wagon plundering it while a 
Lone Bandit with a bloodthirsty look creeps 
closer to the man. You notice a sword at your
feet. Arming yourself, you run in between the
man and the Lone Bandit ready to fight. The
Lone Bandit laughs and readies his knife.''')
        text = message_dialog(
            title='Prologue',
            text='''As the Lone Bandit charges at you, you
feel adrenaline pumping throughout your body
and a surge of energy overflowing through you. You
feel as if your soul is soaring. Time begins
to slow down and knowledge is rushing through
your mind.''')
        text = message_dialog(
            title='Prologue',
            text='''Your soul transforms and becomes the Hero Soul''')
        text = message_dialog(
            title='Prologue',
            text='''The Hero Soul within you imparts the skill Flare to you
Flare will deal Burn DMG damaging both the enemy's health and max Health''')
        text = message_dialog(
            title='Battle',
            text='''Immortal War is a turn-based RPG. This
tutorial will go over how to battle.''')
        text = message_dialog(
            title='Battle', text='Attack deals basic DMG to the enemy.')
        text = message_dialog(
            title='Battle',
            text='''Spells shows all the spells you've learned
and gives you option to choose a spell to
use. Spells are learned by leveling up and
require mana. Mana is recovered by not using
spells for a turn. Flare is the only spell
you have as of right now.''')
        text = message_dialog(
            title='Battle',
            text='''Items will open your bag and lets you use
an item. Items can be bought in the shop.''')
        text = message_dialog(
            title='Battle',
            text='''Wait replenishes mana more than all other
actions and ends your current turn.''')
        text = message_dialog(
            title='Battle',
            text='''Run allows you to escape the battle.
Chances of escaping are based on your
evasion. You can not escape certain
battles.''')
        text = message_dialog(
            title='Battle',
            text='''The battle ends when you or the enemy's
health reaches zero. Good luck.''')
        player = player_stats(character)
        enemy = prologue_enemy()
        # bandit_image()
        scripted_battle(player, enemy, character, bag)
        character = player_reload(character)
    elif game == 'Load':
        save = loads()
        character = load_save(save)
        if character == None:
            text = message_dialog(title='Error', text='No Save')
            main()
        bag = load_inventory(save)
        key_items = load_key_items(save)
        clear()
        system('setterm -cursor off')
        print('\nLoading...\n{} {}\tLevel: {} - Gold: {}\n'.format(
            character['Player']['Gender'], character['Player']['Name'],
            character['Player']['Level'], character['Player']['Gold']))
        loading()
    # gunna put a prologue that ends with the character going to bed
    print('Waking up...')
    while True:
        choices = input(
            '\nWhat would you like to do?\n1 - Character Menu\n2 - Rest\n3 - Leave Home\n>>> '
        )
        if choices == '1':
            character_menu(character, bag)
        elif choices == '2':
            print('Going to sleep...')
            sleep(1)
            save = save_to_file(character)
            bag_to_inventory(bag, save)
            key_items_to_file(key_items, save)
            print('Saving game...')
            sleep(1)
            play = ''
            while play != '1':
                play = input('Quit?\n1 - Yes\n2 - No\n>>> ')
                if play == '1':
                    print('Quitting game...')
                    sleep(1)
                    exit()
                elif play == '2':
                    print('Waking up')
                    sleep(1)
                    break
                else:
                    print('Choose a valid option')
        elif choices == '3':
            print('You leave your home')
            area = ''
            while area != '1':
                area = input(
                    '\nYou head outside into the city\nWhere do you want to go?\n1 - Home\n2 - Shop\n3 - Trainer\n4 - Gate\n>>> '
                )
                if area == '1':
                    'You went home'
                elif area == '2':
                    print('You went to the adventure shop')
                    shop(bag, character)
                elif area == '3':
                    print('Trainer: "Come back when you\'re stronger"')
                elif area == '4':
                    print('You went to city gate')
                    dungeon = ''
                    while dungeon != '1':
                        clear()
                        system('setterm -cursor off')
                        dungeon = input(
                            '\nYou arrived at the gate\nWhere would you like to explore?\n1 - City\n2 - Forest\n>>> '
                        )
                        if dungeon == '1':
                            print('You head back into the city')
                        elif dungeon == '2':
                            print('You head towards the Splinter Forest')
                            if character['Player']['Level'] < 10 or key_items['Bandit Leader\'s Dagger'] == True:
                                enemy = choice(['1', '2', '3'])
                                if enemy == '1':
                                    # goblin_image()
                                    print(
                                        '\nYou\'re being ambushed by a Slow Goblin'
                                    )
                                    player = player_stats(character)
                                    enemy = forest_goblin(player)
                                    battle(player, enemy, character, bag)
                                    character = player_reload(character)
                                elif enemy == '2':
                                    # wolf_image()
                                    print(
                                        '\nYou\'re being hunted by a Starved Wolf'
                                    )
                                    player = player_stats(character)
                                    enemy = starved_wolf(player)
                                    battle(player, enemy, character, bag)
                                    character = player_reload(character)
                                elif enemy == '3':
                                    # bandit_image()
                                    print('\nYou\'re being robbed by a Bandit')
                                    player = player_stats(character)
                                    enemy = forest_bandit(player)
                                    battle(player, enemy, character, bag)
                                    character = player_reload(character)
                            elif character['Player']['Level'] >= 10 and key_items['Bandit Leader\'s Dagger'] == False:
                                enemy = choice(['1', '2', '3', '4'])
                                if enemy == '1':
                                    # goblin_image()
                                    print(
                                        '\nYou\'re being ambushed by a Slow Goblin'
                                    )
                                    player = player_stats(character)
                                    enemy = forest_goblin(player)
                                    battle(player, enemy, character, bag)
                                    character = player_reload(character)
                                elif enemy == '2':
                                    # wolf_image()
                                    print(
                                        '\nYou\'re being hunted by a Starved Wolf'
                                    )
                                    player = player_stats(character)
                                    enemy = starved_wolf(player)
                                    battle(player, enemy, character, bag)
                                    character = player_reload(character)
                                elif enemy == '3':
                                    # bandit_image()
                                    print('\nYou\'re being robbed by a Bandit')
                                    player = player_stats(character)
                                    enemy = forest_bandit(player)
                                    battle(player, enemy, character, bag)
                                    character = player_reload(character)
                                elif enemy == '4':
                                    # bandit_leader_image()
                                    text = message_dialog(
                                        title='Battle',
                                        text=
                                        'You have found the Bandit Leader\nBandit Leader: "Time to die, pig!"'
                                    )
                                    player = player_stats(character)
                                    enemy = bandit_leader()
                                    boss_battle(player, enemy, character, bag)
                                    character = player_reload(character)
                                    key_items['Bandit Leader\'s Dagger'] = True
                                    text = message_dialog(
                                        title='Congratulations',
                                        text=
                                        'You have completed the Beta Version of Immortal War.\nThis is the story so far, but you\'re free to keep playing.'
                                    )

                        else:
                            print('Choose a valid option')
                else:
                    print('Choose a valid option')
        else:
            print('Choose a valid option')


if __name__ == '__main__':
    main()
