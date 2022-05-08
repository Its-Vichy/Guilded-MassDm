import threading, json, time, itertools, math
from colorama import Fore, init, Style; init()
from lib.guildead import Guilded
from lib.console import Console
from lib.data import Data

__config__, __proxies__ = json.load(open('./config.json')), itertools.cycle(list(set(open('./data/proxies.txt', 'r+').read().splitlines())))

class Utils:
    @staticmethod
    def load_accounts(database: Data):
        def check(email: str, password: str, cookie: str):
            api = Guilded(f'http://{next(__proxies__)}')
            success, cookies = api.login(email, password)

            if success:
                database.accounts.append(api)
                Console.printf(f'({cookies["hmac_signed_session"][:30]}) ({len(database.accounts)}) Success login in {Style.BRIGHT}{api.user["name"]}{Style.RESET_ALL}.')

                if __config__['save_valid']:
                    with open('./data/valid.txt', 'a+') as f:
                        f.write(f'{email}:{password}:{cookies["hmac_signed_session"]}\n')
            else:
                if cookies["error"] == "You have been banned.":
                    database.banned_account += 1

                if cookies["error"] == "Email or password is incorrect.":
                    database.invalid_account += 1

                Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) ({len(database.accounts)}) Login failed ({Fore.YELLOW}{cookies["error"]}).')

        combo = list(set(open('./data/cookies.txt', 'r+').read().splitlines()))
        thread_list = []

        Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Loading {Style.BRIGHT}{len(combo)}{Style.RESET_ALL} accounts...\n')
        start_time = time.time()

        for account in combo:
            while threading.active_count() >= __config__['loading_thread']:
                time.sleep(1)

            email, password, cookie = account.split(':')
            t = threading.Thread(target=check, args=[email, password, cookie])
            thread_list.append(t)
            t.start()

        for thread in thread_list:
            thread.join()

        Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Logged in {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL}/{Style.BRIGHT}{len(combo)}{Style.RESET_ALL} accounts in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s, banned: {database.banned_account}, invalid: {database.invalid_account}')
        time.sleep(1) # uwu

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

        Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Joining {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL} accounts...\n')
        start_time = time.time()

        for account in database.accounts:
            while threading.active_count() >= threads:
                time.sleep(1)

            t = threading.Thread(target=join, args=[account])
            thread_list.append(t)
            t.start()

        for thread in thread_list:
            thread.join()

        Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Joined in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s')
        input('press enter...')

    @staticmethod
    def mass_dm(message: str, threads: int, database: Data):
        def dm(api: Guilded, member_id: str):
            cookie = api.session.cookies.get('hmac_signed_session')

            try:
                c_resp = api.open_dm_channel(member_id)

                if 'TooManyRequestsError' in str(c_resp.json()):
                    database.ratelimited += 1
                    Console.printf(f'({Fore.YELLOW}{cookie[:30]}) ({database.ratelimited}) Ratelimited.')
                    return
                else:
                    # time to track errors
                    if c_resp.status_code != 200:
                        Console.debug(c_resp.json())

                channel_id = c_resp.json()['channel']['id']
                resp = api.send_message(channel_id, message)

                if resp.status_code == 200:
                    database.sent_dm += 1
                    Console.printf(f'({cookie[:30]}) ({database.sent_dm}) Success sent dm to {member_id}.')

                    with open('./data/done.txt', 'a+') as f:
                        f.write(f'{member_id}\n')
                        database.sent.append(member_id)
                else:
                    database.error_dm += 1
                    Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) ({database.error_dm}) Failed dm to {member_id}.')
            except Exception as e:
                database.error_dm += 1
                Console.debug(str(e))
                Console.printf(f'({Fore.RED}{cookie[:30]}) ({database.error_dm}) Failed dm to {member_id}.')
                pass

        while True:
            thread_list = []

            Console.printf(f'{Fore.LIGHTGREEN_EX}*~>{Fore.RESET} Starting MassDM on {len(database.ids)} members with {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL} accounts...\n')
            start_time = time.time()
            acc = itertools.cycle(database.accounts)

            for member in database.ids:
                if member in database.sent:
                    continue

                while threading.active_count() >= threads:
                    time.sleep(0.3)

                t = threading.Thread(target=dm, args=[next(acc), member])
                thread_list.append(t)
                t.start()

            for thread in thread_list:
                thread.join()

            Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Sent dm to {len(database.ids)} users in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s, success: {database.sent_dm}, error: {database.error_dm}, ratelimit: {database.ratelimited}')

            if input('restart ? (y/n): ').lower() != 'y':
                break

            Console.print_logo()

    @staticmethod
    def change_pfp(pfp_list: list, threads: int, database: Data):
        pfp = itertools.cycle(pfp_list)

        def change(api: Guilded):
            resp = None
            cookie = api.session.cookies.get('hmac_signed_session')

            resp = api.add_pfp(next(pfp)).status_code

            if resp == 200:
                Console.printf(f'({cookie[:30]}) Successfully changed pfp.')
            else:
                Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) PFP change failed.')

        thread_list = []

        Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Changing pfp of {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL} accounts...\n')
        start_time = time.time()

        for account in database.accounts:
            while threading.active_count() >= threads:
                time.sleep(1)

            t = threading.Thread(target=change, args=[account])
            thread_list.append(t)
            t.start()

        for thread in thread_list:
            thread.join()

        Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Changed pfp in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s')
        input('press enter...')

    @staticmethod
    def settings_page():
        Console.printf(f'{Style.RESET_ALL}{Fore.YELLOW}*~>{Fore.RESET} y = yes, n = no, d = default (don\'t change).\n')

        scrape_cookie = db.scrape_settings['scrape_cookie']
        scrape_default_pfp = db.scrape_settings['scrape_default_pfp']
        with_role_only = db.scrape_settings['with_role_only']
        scrape_online = db.scrape_settings['scrape_online']

        ask_scrape_cookie = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Please provide cookie that was on the server (cookie/d): ')
        ask_scrape_default_pfp = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Scrape account with default pfp (y/n/d): ').lower()
        ask_with_role_only = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Scrape only account with role (y/n/d): ').lower()
        ask_scrape_online = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Scrape only connected account (y/n/d): ').lower()

        if ask_scrape_cookie != 'd':
            db.scrape_settings['scrape_cookie'] = scrape_cookie

        if ask_scrape_default_pfp != 'd':
            db.scrape_settings['scrape_default_pfp'] = True if scrape_default_pfp == 'y' else False

        if ask_scrape_online != 'd':
            db.scrape_settings['scrape_online'] = True if scrape_online == 'y' else False

        if ask_with_role_only != 'd':
            db.scrape_settings['with_role_only'] = True if with_role_only == 'y' else False

        if input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Save settings (y/n): ').lower() == 'y':
            db.save_settings()

if __name__ == '__main__':
    db = Data()

    Console.print_logo()
    Utils.load_accounts(db)
    Console.print_logo()

    while True:
        Console.print_logo()
        Console.print_modules()

        category = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Category:{Style.BRIGHT} ')
        options  = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Option:{Style.BRIGHT} ')

        if not (category.isdigit() and options.isdigit() and 0 <= int(category) <= 4 and 0 <= int(options) <= 3):
            input(f'{Style.RESET_ALL}{Fore.RED}*~>{Fore.RESET} Invalid choice.')
            continue

        category, options = int(category), int(options)
        Console.print_logo()

        # Yes the code was pretty ugly but work, for the moment..
        if category == 0:
            guild_id      = None
            item          = None

            use_settings  = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Use default settings (y/n): ').lower()

            if use_settings != 'y':
                Utils.settings_page()

            scrape_cookie = db.scrape_settings['scrape_cookie']
            scrape_default_pfp = db.scrape_settings['scrape_default_pfp']
            with_role_only = db.scrape_settings['with_role_only']
            scrape_online = db.scrape_settings['scrape_online']

            api = Guilded(f'http://{next(__proxies__)}')
            api.login_from_token(scrape_cookie)

            teams = api.get_me()['teams']

            for i, team in enumerate(teams):
                print(f'#{i} | {team["id"]} | {team["name"]}')

            guild_id = input(f'\n{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} TeamID: ')

            if options == 0:
                item = 'id'
            elif options == 1:
                item = 'profilePicture'
            elif options == 2:
                item = 'name'

            resp = api.get_guild_member(guild_id)

            if resp.status_code is not 200:
                input(f'{Style.RESET_ALL}{Fore.RED}*~>{Fore.RESET} Error when scraping members.')
                Console.debug(resp.json())
                continue

            members = resp.json()['members']
            scrapped = []

            for member in members:
                if 'type' not in str(member):
                    try:
                        if str(item) in member:
                            if member[item]:
                                if 'roleIds' in str(member):
                                    if not member['roleIds'] and with_role_only:
                                        continue

                                if scrape_online:
                                    if 'userPresenceStatus' not in str(member):
                                        continue

                                scrapped.append(member[item])
                    except Exception as e:
                        Console.debug(f'Scrape error: {e}')
                        pass

            scrapped = list(set(scrapped))

            Console.printf(f'\n{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}>{Fore.RESET} Scrapped {Style.BRIGHT}{len(scrapped)}{Style.RESET_ALL} {item}, saving into {Style.BRIGHT}./data/{item}.txt{Style.RESET_ALL}')

            with open(f'./data/{item}.txt', 'a+', encoding='utf-8', errors='ignore') as f:
                for thing in scrapped:
                    f.write(thing.split("\n")[0] + '\n')

            input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Success, press key to continue..')

        if category == 1:
            threads     = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))
            invite      = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} InviteCode/TeamID: ')

            Utils.join_accounts(invite, options, threads, db)

        if category == 2:
            message   = open('./data/message.txt', 'r+', encoding='utf-8', errors='ignore').read()
            threads   = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))

            if db.scrape_settings['scrape_cookie'] != "":
                api = Guilded(f'http://{next(__proxies__)}')
                api.login_from_token(db.scrape_settings['scrape_cookie'])
                teams = api.get_me()['teams']

                for i, team in enumerate(teams):
                    print(f'#{i} | {team["id"]} | {team["name"]}')

            guild_id = input(f'\n{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} TeamID: ')

            db.ids = list(set(open('./data/id.txt').read().splitlines()))
            db.sent_dm = 0
            db.error_dm = 0

            for uuid in db.ids:
                if uuid in db.sent:
                    db.ids.remove(uuid)

            Utils.mass_dm(message, threads, db)

        if category == 3:
            if options == 0:
                pfp = list(set(open('./data/profilePicture.txt', 'r+').read().splitlines()))

                if not pfp:
                    Console.printf(f'{Style.RESET_ALL}{Fore.RED}*~>{Fore.RESET}  Please put provide pfp link in {Style.BRIGHT}profilePicture.txt{Style.RESET_ALL}.')
                else:
                    threads   = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))
                    Utils.change_pfp(pfp, threads, db)

            if options == 1:
                Utils.settings_page()