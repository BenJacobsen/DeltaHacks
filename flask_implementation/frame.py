from flask import Flask, request, Response


class game:
    def __init__(self, url, prompts, prompt_assign): #front_end
        self.players = []
        self.players_in = 0
        self.round_num = 0
        self.max_players = 3
        self.prompts = prompts
        self.prompt_assign = prompt_assign

    def start_round(self):
        sorted_prompts = self.prompt_assign(len(self.players), self.prompts)
        for i in range(0, self.players):
            self.players[i].prompts = sorted_prompts[i]
        

class player:
    def __init__(self, pid, name, prompts):
        self.id = pid
        self.name = name
        self.prompts = prompts
        self.responses = []


