from frame import game, player
IP = "127.0.0.1"
prompts = ['Pick']

def prompt_assign(game):
    return [game.prompts for i in range(game.num_players)]

def round_start_func(game):
    print("Which drink do you prefer?")
    print('A : Coke')
    print('B : Pepsi')
    
def round_end_func(game):
    print('Round' + str(game.round_num)+ ':')
    for key in game.player_keys:
        #answer = game.players[key].responses[game.round_num - 1] == '0' ? 'A' : 'B'
        print(game.players[key].name + ' answered: ' + game.players[key].responses[game.round_num - 1])

def end_func(game):
    print('Round ' + str(game.max_rounds)+ ':')
    for key in game.player_keys:
        print(game.players[key].name + ' answered: ' + game.players[key].responses[game.max_rounds - 1])
    print("GAME OVER")

max_players = 2
max_rounds = 1



if __name__ == '__main__':
    new_game = game(IP, prompts, prompt_assign, round_start_func, round_end_func, end_func, max_players, max_rounds)
    new_game.start()