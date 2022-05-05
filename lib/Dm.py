from lib.guildead import Guilded
import threading

class Dm(threading.Thread):
    def __init__(self, token: str, user_id: str, message: int):
        self.message = message
        self.token = token
        self.user_id = user_id
        self.api = Guilded()

        self.api.login_from_token(self.token, True)
        
        threading.Thread.__init__(self)

    def run(self):
        try:
            channel_id = self.api.open_dm_channel(self.user_id)['channel']['id']
            r = self.api.send_message(channel_id, self.message)
            print(r)
        except:
            pass