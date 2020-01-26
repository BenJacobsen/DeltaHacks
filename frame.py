from flask import Flask, request, Response


class game:
    def __init__(self, url, prompts, prompt_assign, max_players): #front_end
        self.players = {}
        self.player_keys = []
        self.num_players = 0
        self.round_num = 0
        self.num_answers = 0
        self.max_rounds = 2
        self.max_players = max_players
        self.prompts = prompts
        self.prompt_assign = prompt_assign
    
    def setup_after_login(self):
        sorted_prompts = self.prompt_assign(self.num_players, self.prompts)
        for i in range(0, len(self.player_keys)):
            self.players[self.player_keys[i]].prompts = sorted_prompts[i]
        if self.max_rounds == 0:
            for prompt in sorted_prompts:
                if len(prompt) > self.max_rounds:
                    self.max_rounds = len(prompt)

class player:
    def __init__(self, name):
        self.name = name
        self.prompts = []
        self.responses = []


