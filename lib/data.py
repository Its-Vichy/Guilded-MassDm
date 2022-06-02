import json


class Data:
    def __init__(self):
        self.sent_dm = 0
        self.error_dm = 0
        self.ratelimited = 0
        self.accounts = []
        self.ids = []
        self.locked = 0

        self.banned_account = 0
        self.invalid_account = 0

        self.sent = list(set(open('./data/done.txt', 'r+').read().splitlines()))
        self.status = list(set(open('./data/userStatus.txt', 'r+',  encoding='utf-8', errors='ingore').read().splitlines()))
        self.bio = list(set(open('./data/userBio.txt', 'r+', encoding='utf-8', errors='ingore').read().splitlines()))
        
        self.locked_dm = list(set(open('./data/locked_dm.txt', 'r+').read().splitlines()))

        self.scrape_settings = json.load(open('./settings/scrape_settings.json', 'r+'))

    def save_settings(self):
        with open('./settings/scrape_settings.json', 'w+') as fp:
            json.dump(self.scrape_settings, fp,  indent=4)