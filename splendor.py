from collections import OrderedDict
import sys
import re

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

def take_gems(num_gems, color):
  string_format = 'You took {} {} gem'

  if num_gems <= 0:
    print('{} is not a valid number'.format(num_gems))
    return
  elif num_gems > 1:
    # pluralize the word 'gem'
    string_format += 's'

  print(string_format.format(num_gems, color))

# main
num_players = input("Enter the number of players: ")
gems = determine_starting_gems(int(num_players))
print("The starting gems will be " + dict_to_pretty_str(gems) + '\n')

while True:
  print(help_string(gems))
  action = input('Enter an action\n').strip()

  if action.lower() == 'quit':
    print('Thanks for playing!')
    sys.exit()

  take_gems_pattern = '^take (\d+) (\w+)'
  match = re.search(take_gems_pattern, action)

  if match:
    take_gems(int(match.group(1)), match.group(2))

