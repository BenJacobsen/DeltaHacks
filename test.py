from frame import game, player
IP = "127.0.0.1"
prompts = ['Favorite Sport?', 'Favorite Food?']

def prompt_assign(game):
    return [[game.prompts[0], game.prompts[1]] for i in range(game.num_players)]

def round_start_func(game):
    return
    
def round_end_func(game):
    print('Round' + str(game.round_num)+ ':')
    for key in game.player_keys:
        print(game.players[key].name + ' said: ' + game.players[key].responses[game.round_num - 1])

def end_func(game):
    print("GAME OVER")
    print("ROUND RECAPS:")
    for i in range(1, game.round_num + 1):
        print('Round ' + str(i) + ':')
        for key in game.player_keys:
            print(game.players[key].name + ' said: ' + game.players[key].responses[i - 1])

max_players = 2
max_rounds = 2



if __name__ == '__main__':
    new_game = game(IP, prompts, prompt_assign, round_start_func, round_end_func, end_func, max_players, max_rounds)
    new_game.start()