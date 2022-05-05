from re import A
import threading, json, time, itertools, math, os
from colorama import Fore, init, Style; init()
from lib.guildead import Guilded

__lock__, __config__, __proxies__ = threading.Lock(), json.load(open('./config.json')), itertools.cycle(list(set(open('./data/proxies.txt', 'r+').read().splitlines())))

class Data:
    def __init__(self):
        self.sent_dm = 0
        self.error_dm = 0
        self.accounts = []
        self.ids = []

class Console:
    @staticmethod
    def print_logo():
        os.system('cls && title G-MassDM' if os.name == 'nt' else 'clear')
        print(f'''
 {Fore.YELLOW}  ____ {Fore.LIGHTWHITE_EX}    __  __              {Fore.YELLOW} ____  __  __ {Fore.LIGHTWHITE_EX}
 {Fore.YELLOW} / ___|{Fore.LIGHTWHITE_EX}   |  \/  | __ _ ___ ___{Fore.YELLOW}|  _ \|  \/  |{Fore.LIGHTWHITE_EX}
 {Fore.YELLOW}| |  _ {Fore.LIGHTWHITE_EX}___| |\/| |/ _` / __/ __{Fore.YELLOW}| | | | |\/| |{Fore.LIGHTWHITE_EX}
 {Fore.YELLOW}| |_| |{Fore.LIGHTWHITE_EX}___| |  | | (_| \__ \__ \{Fore.YELLOW} |_| | |  | |{Fore.LIGHTWHITE_EX}
 {Fore.YELLOW} \____|{Fore.LIGHTWHITE_EX}   |_|  |_|\__,_|___/___/{Fore.YELLOW}____/|_|  |_|{Fore.LIGHTWHITE_EX} {Style.BRIGHT}github.com/its-vichy{Style.RESET_ALL}
        
        ''')

    @staticmethod
    def printf(content: str):
        __lock__.acquire()
        print(content.replace('(', f'({Fore.LIGHTBLUE_EX}').replace(')', f'{Fore.RESET})'))
        __lock__.release()

    @staticmethod
    def print_modules():
        print(f'''  > Options:
        [{Fore.YELLOW}0{Fore.LIGHTWHITE_EX}] Scraper:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Scrape id.
            - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Scrape avatars.
            - [{Fore.LIGHTBLUE_EX}2{Fore.LIGHTWHITE_EX}] Scrape usernames.
            
        [{Fore.YELLOW}1{Fore.LIGHTWHITE_EX}] Joiner:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Join guild.
            - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Join team.
            
        [{Fore.YELLOW}2{Fore.LIGHTWHITE_EX}] MassDM:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Mass DM guild.
            - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Single DM Spam.
        ''')

class Utils:
    @staticmethod
    def load_accounts(database: Data):
        def check(email: str, password: str, cookie: str):
            api = Guilded(f'http://{next(__proxies__)}')
            success, cookies = api.login(email, password)

            if success:
                database.accounts.append(api)
                Console.printf(f'({cookies["hmac_signed_session"][:30]}) Success login in {Style.BRIGHT}{api.user["name"]}{Style.RESET_ALL}.')
            else:
                Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) Login failed.')

        combo = list(set(open('./data/cookies.txt', 'r+').read().splitlines()))
        thread_list = []

        Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Loading {Style.BRIGHT}{len(combo)}{Style.RESET_ALL} accounts...\n')
        start_time = time.time()

        for account in combo:
            while threading.active_count() >= __config__['loading_thread']:
                time.sleep(1)

            email, password, cookie = account.split(':')
            T = threading.Thread(target=check, args=[email, password, cookie])
            thread_list.append(T)
            T.start()
            
        for thread in thread_list:
            thread.join()
        
        Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Logged in {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL}/{Style.BRIGHT}{len(combo)}{Style.RESET_ALL} accounts in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s')
        time.sleep(3)
    
    @staticmethod
    def join_accounts(invite: str, type: int, threads: int, database: Data):
        def join(api: Guilded):
            resp = None
            cookie = api.session.cookies.get('hmac_signed_session')

            if type == 0:
                resp = api.join_server(invite).status_code
            else:
                resp = api.join_team(invite).status_code
            
            if resp == 200:
                Console.printf(f'({cookie[:30]}) Success join.')
            else:
                Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) Join failed.')

        thread_list = []

        Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Joining with {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL} accounts...\n')
        start_time = time.time()

        for account in database.accounts:
            while threading.active_count() >= threads:
                time.sleep(1)
                
            T = threading.Thread(target=join, args=[account])
            thread_list.append(T)
            T.start()
            
        for thread in thread_list:
            thread.join()
        
        Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Joined in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s')
        time.sleep(3)

    @staticmethod
    def mass_dm(message: str, threads: int, database: Data):
        def dm(api: Guilded, member_id: str):
            cookie = api.session.cookies.get('hmac_signed_session')

            try:
                channel_id = api.open_dm_channel(member_id).json()['channel']['id']
                resp = api.send_message(channel_id, message)
                
                if resp.status_code == 200:
                    database.sent_dm += 1
                    Console.printf(f'({cookie[:30]}) ({database.sent_dm}) Success sent dm to {member_id}.')
                else:
                    database.error_dm += 1
                    Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) ({database.error_dm}) Failed dm to {member_id}.')
            except:
                database.error_dm += 1
                Console.printf(f'({Fore.RED}{cookie[:30]}) ({database.error_dm}) Failed dm to {member_id}.')
                pass

        thread_list = []

        Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Starting MassDM on {len(database.ids)} members with {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL} accounts...\n')
        start_time = time.time()
        acc = itertools.cycle(database.accounts)

        for member in database.ids:
            while threading.active_count() >= threads:
                time.sleep(1)
                
            T = threading.Thread(target=dm, args=[next(acc), member])
            thread_list.append(T)
            T.start()
            
        for thread in thread_list:
            thread.join()
        
        Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Sent dm to {len(database.ids)} users in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s')
        time.sleep(6)


if __name__ == '__main__':
    db = Data()
    
    Console.print_logo()
    Utils.load_accounts(db)
    Console.print_logo()

    while True:
        Console.print_logo()
        Console.print_modules()
        
        category = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Category:{Style.BRIGHT} '))
        options  = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Option:{Style.BRIGHT} '))
        
        Console.print_logo()

        if category == 0:
            scrape_cookie = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Please provide cookie that was on the server: ')
            guild_id      = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} GuildID/TeamID: ')
            item          = None

            api = Guilded(f'http://{next(__proxies__)}')
            api.login_from_token(scrape_cookie)

            if options == 0:
                item = 'id'
            elif options == 1:
                item = 'profilePicture'
            elif options == 2:
                item = 'name'
            
            members = api.get_guild_member(guild_id).json()['members']
            scrapped = []

            for member in members:
                if 'type' not in str(member):
                    try:
                        scrapped.append(member[item])
                    except:
                        pass

            scrapped = list(set(scrapped))
            
            Console.printf(f'\n{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}>{Fore.RESET} Scrapped {Style.BRIGHT}{len(scrapped)}{Style.RESET_ALL} {item}, saving into {Style.BRIGHT}./data/{item}.txt{Style.RESET_ALL}')

            with open(f'./data/{item}.txt', 'a+') as f:
                for thing in scrapped:
                    f.write(thing.split("\n")[0] + '\n')
            
            input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Success, press key to continue..')
        
        if category == 1:
            threads     = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))
            invite      = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} InviteCode/TeamID: ')

            Utils.join_accounts(invite, options, threads, db)
        
        if category == 2:
            message   = open('./data/message.txt', 'r+').read()
            threads   = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))
            guild_id  = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} GuildID/TeamID: ')

            db.ids = list(set(open('./data/id.txt').read().splitlines()))
            db.sent_dm = 0
            db.error_dm = 0

            Utils.mass_dm(message, threads, db)