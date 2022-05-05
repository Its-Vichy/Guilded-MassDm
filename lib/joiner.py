from lib.guildead import Guilded
import threading

class Joiner(threading.Thread):
    def __init__(self, token: str, invite_code: str, type: int):
        self.type = type
        self.token = token
        self.invite_code = invite_code
        self.api = Guilded()

        self.api.login_from_token(self.token, True if self.type == 1 else False)
        
        threading.Thread.__init__(self)
    
    def run(self):
        if self.type == 0:
            self.api.join_server(self.invite_code)
        
        if self.type == 1:
            self.api.join_team(self.invite_code)
        
        print(f'[Joined] {self.invite_code} -> {self.token[:30]}')