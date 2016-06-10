from collections import OrderedDict
import sys
import re
import copy

GEM_COLORS = {'black', 'blue', 'green', 'red', 'white', 'yellow'}

class Player:
  def __init__(self):
    self.gems = {c : 0 for c in GEM_COLORS}

def determine_starting_gems(num_players):
  if num_players < 2 or num_players > 4:
    raise ValueError('There must be 2-4 players')

  four_player_gems = {c : 7 for c in GEM_COLORS}

  # reduce starting gems appropriate to the player count
  if num_players == 2:
    result = reduce_gems(3, four_player_gems)
  elif num_players == 3:
    result = reduce_gems(2, four_player_gems)
  else:
    result = four_player_gems

  # yellow/wild gems are never reduced
  result['yellow'] = 5
  return OrderedDict(sorted(result.items()))

def reduce_gems(reduction, gems):
  return {k : v - reduction for k, v in gems.items()}

def dict_to_pretty_str(d):
  separator = ', '
  format_string = '{}:{}'
  return separator.join(format_string.format(k, v) for k, v in d.items())

def help_string(gems, player):
  current_state_string = 'Available gems - ' + dict_to_pretty_str(gems) + '\n\n'
  current_state_string += 'Player currently has - ' + dict_to_pretty_str(player.gems)

  help_string = '''Possible Actions:
    1) take <color1> <color2> <color3> - Take 3 gems, each of different colors. ex: take black blue red
    2) quit - Quit the program'''

  return current_state_string + '\n\n' + help_string + '\n'

def take_different_gems(colors_list, gems_state, player):
  for color in colors_list:
    if color not in GEM_COLORS:
      print('{} is not a valid color'.format(color))
      return gems_state

  for color in colors_list:
    if gems_state[color] == 0:
      print('There are no more {} gems'.format(color))
      return gems_state

  colors_set = set(colors_list)

  if 'yellow' in colors_set:
    print('Yellow gems cannot be taken directly')
    return gems_state

  if len(colors_set) != len(colors_list):
    print('Cannot take more than one from a color')
    return gems_state

  taken_gems_str = ', '.join(c for c in colors_list)
  print('You took {} gems'.format(taken_gems_str))

  new_gems_state = copy.deepcopy(gems_state)
  new_player = copy.deepcopy(player)
  for color in colors_list:
    new_gems_state[color] -= 1
    new_player.gems[color] += 1
  return (new_gems_state, new_player)

# main
num_players = input("Enter the number of players> ")
gems_state = determine_starting_gems(int(num_players))
# TODO: implement multiple players
player = Player()
print("The starting gems will be " + dict_to_pretty_str(gems_state) + '\n')

while True:
  print(help_string(gems_state, player))
  action = input('Enter an action> ').strip()

  if action.lower() == 'quit':
    print('Thanks for playing!')
    sys.exit()

  take_different_gems_pattern = '^take (\w+) (\w+) (\w+)$'
  match = re.search(take_different_gems_pattern, action)

  if match:
    result = take_different_gems(
              [match.group(1), match.group(2), match.group(3)],
              gems_state,
              player)
    gems_state = result[0]
    player = result[1]

