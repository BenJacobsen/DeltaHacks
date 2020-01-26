from frame import game, player

def prompt_assign(num_players, prompts):
    return [[prompts[0], prompts[1]] for i in range(num_players)]

if __name__ == '__main__':
    gamer = game('localhost', ['Favorite Sport?', 'Favorite Food?'], prompt_assign)
 #   gamer.start()