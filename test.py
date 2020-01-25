from frame import game, player

def prompt_assign(num_players, prompts):
    return [[prompts[0], prompts[1]] for i in range(num_players)]


game('localhost', ['Favorite Sport?', 'Favorite Food?'], prompt_assign)

game.start()