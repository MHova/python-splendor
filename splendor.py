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
  return result

def reduce_gems(reduction, gems):
  return {k : v - reduction for k, v in gems.items()}

num_players = input("Enter the number of players: ")
print("The starting gems will be: " + str(determine_starting_gems(int(num_players))))
