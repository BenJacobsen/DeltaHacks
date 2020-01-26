from flask import Flask, request, Response, g
from frame import game, player
def prompt_assign(num_players, prompts):
    return [[prompts[0], prompts[1]] for i in range(num_players)]


app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def login(): # mutexify
    if g.gamer.players_in < g.gamer.max_players:
        g.gamer.players_in += 1
        this_id = g.gamer.players_in
        g.gamer.players.append(player(g.gamer.players_in, request.data.name))
        #await for others/ prompts to be assigned
        return Response(response=jsonpickle.encode({"data":{"id":g.gamer.players[this_id].id, "prompt":g.gamer.players[this_id][round_num]}, "errMsg": ""}), status=200, mimetype="application/json")
    else:
        return Response(response=jsonpickle.encode({"errMsg": "Too many in game"}), status=400, mimetype="application/json")

@app.route('/', methods=['GET'])
def base():
    return g.max_players
if __name__ == '__main__':
    g.gamer = game('localhost', ['Favorite Sport?', 'Favorite Food?'], prompt_assign)
    app.run(debug=True)