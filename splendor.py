from collections import OrderedDict
import sys
import re
import copy

def determine_starting_gems(num_players):
  if num_players < 2 or num_players > 4:
    raise ValueError('There must be 2-4 players')

  four_player_gems = {'black' : 7,
                      'blue'  : 7,
                      'green' : 7,
                      'red'   : 7,
                      'white' : 7}

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

def help_string(gems):
  current_state_string = 'Available gems - ' + dict_to_pretty_str(gems)

  help_string = '''Possible Actions:
    1) take <num gems> <color> - Take gems of the specified color. ex: take 3 black
    2) quit - Quit the program'''

  return current_state_string + '\n\n' + help_string + '\n'

def take_different_gems(colors_list, gems_state):
  for color in colors_list:
    if color not in gems_state:
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

  new_state = copy.deepcopy(gems_state)
  for color in colors_list:
    new_state[color] = new_state[color] - 1
  return new_state

# main
num_players = input("Enter the number of players: ")
gems_state = determine_starting_gems(int(num_players))
print("The starting gems will be " + dict_to_pretty_str(gems_state) + '\n')

while True:
  print(help_string(gems_state))
  action = input('Enter an action\n').strip()

  if action.lower() == 'quit':
    print('Thanks for playing!')
    sys.exit()

  take_different_gems_pattern = '^take (\w+) (\w+) (\w+)$'
  match = re.search(take_different_gems_pattern, action)

  if match:
    gems_state = take_different_gems(
                  [match.group(1), match.group(2), match.group(3)], gems_state)

