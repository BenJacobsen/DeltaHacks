from flask import Flask, request, Response

class game:
    def __init__(self, url, prompts, prompt_assign):
        self.players = []
        self.players_in = 0
        self.max_players = 3
        self.prompts = prompts
        self.prompt_assign = prompt_assign
        app = Flask(__name__)

    @app.route('/api/login', methods=['POST'])
    def login(): # get name etc..
        if (self.players_in < self.max_players):
            self.players_in += 1
            self.players.append(player(self.players_in, request.data.name))
            #await for others
            
        else:
            return Response(response={"errMsg": "Too many in game"}, status=400, mimetype="application/json")
        


        self.start_round()
        #
    
    @app.route('/')
    def base():
        #frontend
    
        #

    def start():
        app.run(debug=True) ## wait for 
        while(players_in < )
    
    def start_round():
        sorted_prompts = self.prompt_assign(len(self.players), self.prompts)
        for i in range(0, self.players):
            self.players[i].prompts = sorted_prompts[i]
        

class player:
    def __init__(self, pid, name, prompts):
        self.id = pid
        self.name = name
        self.prompts = prompts


