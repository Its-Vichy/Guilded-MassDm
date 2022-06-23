import json, os, threading, time

__version__ = '0.0.7'

class Data:
    def __init__(self):
        self.sent_dm = 0
        self.error_dm = 0
        self.ratelimited = 0
        self.accounts = []
        self.ids = []
        self.locked = 0

        self.blacklisted_cookie = []

        self.banned_account = 0
        self.invalid_account = 0

        self.sent = list(set(open('./data/done.txt', 'r+').read().splitlines()))
        self.status = list(set(open('./data/userStatus.txt', 'r+',  encoding='utf-8', errors='ingore').read().splitlines()))
        self.bio = list(set(open('./data/userBio.txt', 'r+', encoding='utf-8', errors='ingore').read().splitlines()))
        
        self.accounts_ids = []
        self.locked_dm = list(set(open('./data/locked_dm.txt', 'r+').read().splitlines()))

        self.scrape_settings = json.load(open('./settings/scrape_settings.json', 'r+'))
        self.proxy_settings = json.load(open('./settings/proxy_settings.json', 'r+'))

        if os.name == 'nt':
            threading.Thread(target=self.win_title_thread).start()
        else:
            threading.Thread(target=self.lin_title_thread).start()
            
    def save_settings(self):
        with open('./settings/scrape_settings.json', 'w+') as fp:
            json.dump(self.scrape_settings, fp,  indent=4)
        
        with open('./settings/proxy_settings.json', 'w+') as fp:
            json.dump(self.proxy_settings, fp,  indent=4)
    
    def win_title_thread(self):
        while True:
            time.sleep(0.5)
            os.system(f'title G-MassDM - {__version__} ^| Accounts: {len(self.accounts)} (Blacklist: {len(self.blacklisted_cookie)}) Ratelimited: {self.ratelimited} DM-Sent: {self.sent_dm} Dm-Err: {self.error_dm} Dm-Lock: {self.locked}')
    
    def lin_title_thread(self):
        while True:
            time.sleep(0.5)
            print(f'\33]0;G-MassDM - {__version__} | Accounts: {len(self.accounts)} (Blacklist: {len(self.blacklisted_cookie)}) Ratelimited: {self.ratelimited} DM-Sent: {self.sent_dm} Dm-Err: {self.error_dm} Dm-Lock: {self.locked}\a', end='', flush=True)