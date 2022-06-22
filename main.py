import threading, json, time, itertools, math, random, httpx
from colorama import Fore, init, Style; init()
from lib.guildead import Guilded
from lib.console import Console
from lib.data import Data

__config__, __proxy_config__, __proxies__ = json.load(open('./settings/config.json')), json.load(open('./settings/proxy_settings.json')), itertools.cycle([])

# yes it can be improved lot of copy/past on other functions
class Utils:
    @staticmethod
    def load_proxies():
        pl = list(set(open('./data/proxies.txt', 'r+').read().splitlines()))

        if __proxy_config__['overwrite_valid_proxies'] and __proxy_config__['check_proxies']:
            with open('./data/proxies.txt', 'w+') as f:
                f.truncate(0)

        def check(proxy: str):
            checking_start_time = time.time()

            try:
                httpx.get('https://www.guilded.gg', proxies='http://'+proxy, timeout= httpx.Timeout(__proxy_config__['proxy_timeout'], connect=__proxy_config__['proxy_connect_timeout']))
                Console.printf(f'({Fore.LIGHTCYAN_EX}{len(pl)}{Fore.RESET}) ({proxy}) {Fore.LIGHTGREEN_EX}Online{Fore.RESET}, {Style.BRIGHT}{math.floor(time.time() - checking_start_time)}{Style.RESET_ALL}s.')
            
                with open('./data/proxies.txt', 'a+') as f:
                    f.write(f'{proxy}\n')
                    f.close()

            except Exception as e:
                Console.printf(f'({Fore.LIGHTCYAN_EX}{len(pl)}{Fore.RESET}) ({proxy}) {Fore.LIGHTRED_EX}Dead.{Fore.RESET}')
                pl.remove(proxy)
                pass
        
        if __proxy_config__['scrape_proxies']:
            base = len(pl)

            for url in list(set(open('./data/proxy_urls.txt', 'r+').read().splitlines())):
                for proxy in list(set(httpx.get(url).text.split('\n'))):
                    pl.append(proxy.split('\n')[0].strip())

            Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Scrapped {Style.BRIGHT}{len(pl)-base}{Style.RESET_ALL} proxies.\n')

        pln = len(pl)

        if __proxy_config__['check_proxies']:
            thread_list = []

            Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Checking {Style.BRIGHT}{pln}{Style.RESET_ALL} proxies...\n')
            start_time = time.time()

            for proxy in pl:
                while threading.active_count() >= __proxy_config__['proxy_checking_thread']:
                    time.sleep(1)

                t = threading.Thread(target=check, args=[proxy])
                thread_list.append(t)
                t.start()

            for thread in thread_list:
                thread.join()

            Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Working proxies: {Style.BRIGHT}{len(pl)}{Style.RESET_ALL}/{Style.BRIGHT}{pln}{Style.RESET_ALL}, checked in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s')
            time.sleep(2)
            
        return itertools.cycle(pl)

    @staticmethod
    def load_accounts(database: Data):
        combo = list(set(open('./data/cookies.txt', 'r+').read().splitlines()))

        def check(email: str, password: str, cookie: str, user_id: str):
            while True:
                try:
                    api = Guilded(__proxies__)

                    if __config__['login']:
                        success, cookies = api.login(email, password)
                    else:
                        cookies = {}

                        api.login_from_token(cookie)
                        success, cookies['hmac_signed_session'] = True, cookie
                        api.user_id = user_id
                    
                    database.accounts_ids.append(api.user_id)

                    if success:
                        database.accounts.append(api)
                        Console.printf(f'({cookies["hmac_signed_session"][:30]}) ({len(database.accounts)}) Success login in {Style.BRIGHT}{api.user["name"] if __config__["login"] else "token"}{Style.RESET_ALL}.')

                        if __config__['save_valid']:
                            with open('./data/valid.txt', 'a+') as f:
                                f.write(f'{email}:{password}:{cookies["hmac_signed_session"]}\n')
                    else:
                        if cookies["error"] == "You have been banned.":
                            database.banned_account += 1

                        if cookies["error"] == "Email or password is incorrect.":
                            database.invalid_account += 1

                        Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) ({len(database.accounts)}) Login failed ({Fore.YELLOW}{cookies["error"]}).')

                    break
                except Exception as e:
                    Console.debug(str(e))
                    continue

        thread_list = []

        Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Loading {Style.BRIGHT}{len(combo)}{Style.RESET_ALL} accounts...\n')
        start_time = time.time()

        for account in combo:
            while threading.active_count() >= __config__['loading_thread']:
                time.sleep(1)

            email, password, cookie, user_id = account.split(':')
            database.accounts_ids.append(user_id)
            t = threading.Thread(target=check, args=[email, password, cookie, user_id])
            thread_list.append(t)
            t.start()

        for thread in thread_list:
            thread.join()

        Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Logged in {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL}/{Style.BRIGHT}{len(combo)}{Style.RESET_ALL} accounts in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s, banned: {database.banned_account}, invalid: {database.invalid_account}')
        time.sleep(2) # uwu

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
    def mass_dm(message: str, threads: int, database: Data, single_mod: bool = False):
        cookie_blacklist = []

        def dm(api: Guilded, member_id: str):
            cookie = api.session.cookies.get('hmac_signed_session')

            if cookie in cookie_blacklist or member_id in database.locked_dm:
                return

            try:
                c_resp = api.open_dm_channel(member_id)

                if 'TooManyRequestsError' in str(c_resp.json()):
                    database.ratelimited += 1
                    Console.printf(f'({Fore.YELLOW}{cookie[:30]}) ({database.ratelimited}) Ratelimited.')
                    cookie_blacklist.append(cookie)
                else:
                    if c_resp.status_code == 412 and "Not allowed to send message" in str(c_resp.json()):
                        Console.printf(f'({Fore.CYAN}{cookie[:30]}) ({database.locked}) dm channels locked.')

                        with open('./data/locked_dm.txt', 'a+') as f:
                            f.write(f'{member_id}\n')
                            database.locked_dm.append(member_id)
                            database.locked += 1

                        database.error_dm += 1

                        if single_mod:
                            cookie_blacklist.append(cookie)
                        return

                    # time to track errors
                    if c_resp.status_code != 200:
                        database.error_dm += 1
                        Console.printf(f'({Fore.MAGENTA}{cookie[:30]}) ({database.error_dm}) Error when oppening dm channel.')
                        Console.debug(c_resp.json())
                        return

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
                        Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) ({database.error_dm}) Failed dm to {member_id} ({resp.json()}).')

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
                if member in database.sent and not single_mod or member in database.locked_dm or member in database.accounts_ids:
                    continue

                while threading.active_count() >= threads:
                    time.sleep(0.3)
                
                t = threading.Thread(target=dm, args=[next(acc), member])
                thread_list.append(t)
                t.start()

            for thread in thread_list:
                thread.join()

            Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Sent dm to {len(database.ids)} users in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s, success: {database.sent_dm}, error: {database.error_dm}, ratelimit: {database.ratelimited}, locked dm: {database.locked}')

            if input('restart with whitelisted accounts ? (y/n): ').lower() != 'y':
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
    def set_online(threads: int, database: Data):
        def change(api: Guilded):
            cookie = api.session.cookies.get('hmac_signed_session')

            r1 = api.set_activity(random.randint(1, 3))

            if r1.status_code == 200:
                Console.printf(f'({cookie[:30]}) Successfully set activity.')
            else:
                Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) Set activity failed.')
            
            r2 = api.ping()

            if r2.status_code == 200:
                Console.printf(f'({cookie[:30]}) Successfully sent ping.')
            else:
                Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) Ping failed.')

        thread_list = []

        Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Starting onliner on {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL} accounts...\n')
        start_time = time.time()

        for account in database.accounts:
            while threading.active_count() >= threads:
                time.sleep(1)

            t = threading.Thread(target=change, args=[account])
            thread_list.append(t)
            t.start()

        for thread in thread_list:
            thread.join()

        Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Job done in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s')
        input('press enter...')

    @staticmethod
    def set_status(threads: int, database: Data):
        status = itertools.cycle(database.status)

        def change(api: Guilded):
            cookie = api.session.cookies.get('hmac_signed_session')

            r1 = api.set_status(next(status), random.randint(90002200, 90002539)) # https://raw.githubusercontent.com/GuildedAPI/datatables/main/reactions.json

            if r1.status_code == 200:
                Console.printf(f'({cookie[:30]}) Successfully set status.')
            else:
                Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) Set status failed.')

        thread_list = []

        Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Set status on {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL} accounts...\n')
        start_time = time.time()

        for account in database.accounts:
            while threading.active_count() >= threads:
                time.sleep(1)

            t = threading.Thread(target=change, args=[account])
            thread_list.append(t)
            t.start()

        for thread in thread_list:
            thread.join()

        Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Job done in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s')
        input('press enter...')
    
    @staticmethod
    def set_bio(threads: int, database: Data):
        bio = itertools.cycle(database.bio)

        def change(api: Guilded):
            cookie = api.session.cookies.get('hmac_signed_session')

            r1 = api.set_bio(next(bio))

            if r1.status_code == 200:
                Console.printf(f'({cookie[:30]}) Successfully set bio.')
            else:
                Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) Set bio failed.')

        thread_list = []

        Console.printf(f'{Fore.YELLOW}*~>{Fore.RESET} Set bio on {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL} accounts...\n')
        start_time = time.time()

        for account in database.accounts:
            while threading.active_count() >= threads:
                time.sleep(1)

            t = threading.Thread(target=change, args=[account])
            thread_list.append(t)
            t.start()

        for thread in thread_list:
            thread.join()

        Console.printf(f'\n{Fore.LIGHTGREEN_EX}+~>{Fore.RESET} Job done in {Style.BRIGHT}{math.floor(time.time() - start_time)}{Style.RESET_ALL}s')
        input('press enter...')

    @staticmethod
    def settings_page():
        Console.printf(f'{Style.RESET_ALL}{Fore.YELLOW}*~>{Fore.RESET} y = yes, n = no, d = default (don\'t change).\n')

        ask_scrape_cookie = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Please provide cookie that was on the server (cookie/d): ')
        ask_scrape_default_pfp = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Scrape account with default pfp (y/n/d): ').lower()
        ask_with_role_only = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Scrape only account with role (y/n/d): ').lower()
        ask_scrape_online = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Scrape only connected account (y/n/d): ').lower()
        join_main  = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Join scrapped servers with main account (y/n/d): ').lower()
        max_scrape  = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Scrape amount (default: 10/d): ')
        min_member = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Mimimum server member scrape (number/d): ')

        if str(max_scrape) != 'd':
            if max_scrape is None:
                max_scrape = 10

            db.scrape_settings['max_scrape'] = int(max_scrape)

        if str(min_member) != 'd':
            db.scrape_settings['min_member'] = int(min_member)

        if join_main != 'd':
            db.scrape_settings['join_main'] = join_main

        if ask_scrape_cookie != 'd':
            db.scrape_settings['scrape_cookie'] = ask_scrape_cookie

        if ask_scrape_default_pfp != 'd':
            db.scrape_settings['scrape_default_pfp'] = True if ask_scrape_default_pfp == 'y' else False

        if ask_scrape_online != 'd':
            db.scrape_settings['scrape_online'] = True if ask_scrape_online == 'y' else False

        if ask_with_role_only != 'd':
            db.scrape_settings['with_role_only'] = True if ask_with_role_only == 'y' else False

        if input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Save settings (y/n): ').lower() == 'y':
            db.save_settings()
    
    @staticmethod
    def proxy_settings_page():
        Console.printf(f'{Style.RESET_ALL}{Fore.YELLOW}*~>{Fore.RESET} y = yes, n = no, d = default (don\'t change).\n')

        proxy_checking_thread = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Proxy checking threads (number/d): ')
        check_proxies = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Check proxy (y/n/d): ').lower()
        scrape_proxies = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Scrape proxy (y/n/d): ').lower()
        overwrite_valid_proxies = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Overwrite valid proxies (y/n/d): ').lower()
        proxy_timeout  = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Proxy timeout (number/d): ')
        proxy_connect_timeout = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Proxy connection timeout (number/d): ')

        if str(proxy_checking_thread) != 'd':
            db.proxy_settings['proxy_checking_thread'] = int(proxy_checking_thread)
        
        if str(proxy_connect_timeout) != 'd':
            db.proxy_settings['proxy_connect_timeout'] = int(proxy_connect_timeout)
        
        if str(proxy_timeout) != 'd':
            db.proxy_settings['proxy_timeout'] = int(proxy_timeout)

        if overwrite_valid_proxies != 'd':
            db.proxy_settings['overwrite_valid_proxies'] = True if overwrite_valid_proxies == 'y' else False

        if check_proxies != 'd':
            db.proxy_settings['check_proxies'] = True if check_proxies == 'y' else False

        if scrape_proxies != 'd':
            db.proxy_settings['scrape_proxies'] = True if scrape_proxies == 'y' else False

        if input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Save settings (y/n): ').lower() == 'y':
            db.save_settings()

    @staticmethod
    def get_teams():
        if db.scrape_settings['scrape_cookie'] != "":
            api = Guilded(__proxies__)
            api.login_from_token(db.scrape_settings['scrape_cookie'])
            teams = api.get_me()['teams']

            print('')

            for i, team in enumerate(teams):
                print(f' #{i} | {team["id"]} | {team["name"]}')

    @staticmethod
    def channel_spam(message: str, channel_id: str, threads: int, database: Data, single_mod: bool = False):
        cookie_blacklist = []
        database.sent_dm = 0

        def send(api: Guilded):
            cookie = api.session.cookies.get('hmac_signed_session')

            if cookie in cookie_blacklist:
                return

            try:
                resp = api.send_message(channel_id, message)

                if resp.status_code == 200:
                    database.sent_dm += 1
                    Console.printf(f'({cookie[:30]}) ({database.sent_dm}) Success sent.')
                elif 'TooManyRequestsError' in str(resp.json()):
                    database.ratelimited += 1
                    Console.printf(f'({Fore.YELLOW}{cookie[:30]}) ({database.ratelimited}) Ratelimited.')
                    cookie_blacklist.append(cookie)
                else:
                    database.error_dm += 1
                    Console.printf(f'({Fore.LIGHTRED_EX}{cookie[:30]}) ({database.error_dm}) Failed ({resp.json()}).')

                    if 'ForbiddenError' or 'NotFoundError' in str(resp.json()):
                        cookie_blacklist.append(cookie)

            except Exception as e:
                database.error_dm += 1
                Console.debug(str(e))
                Console.printf(f'({Fore.RED}{cookie[:30]}) ({database.error_dm}) Failed.')
                pass

        while True:
            Console.printf(f'{Fore.LIGHTGREEN_EX}*~>{Fore.RESET} Starting ChannelSPAM with {Style.BRIGHT}{len(database.accounts)}{Style.RESET_ALL} accounts...\n')
            acc = itertools.cycle(database.accounts)

            while True:
                while threading.active_count() >= threads:
                    time.sleep(0.3)
                
                threading.Thread(target=send, args=[next(acc)]).start()


if __name__ == '__main__':
    db = Data()

    if __config__['overwrite_valid']:
        with open('./data/valid.txt', 'w+') as f:
            f.truncate(0)

    Console.print_logo()
    __proxies__ = Utils.load_proxies()
    Console.print_logo()
    Utils.load_accounts(db)
    Console.print_logo()

    while True:
        Console.print_logo()
        Console.print_modules()

        category = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Category:{Style.BRIGHT} ')
        options  = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Option:{Style.BRIGHT} ')

        if not (category.isdigit() and options.isdigit() and 0 <= int(category) <= 4 and 0 <= int(options) <= 6):
            input(f'{Style.RESET_ALL}{Fore.RED}*~>{Fore.RESET} Invalid choice.')
            continue

        category, options = int(category), int(options)
        Console.print_logo()

        # Yes the code was pretty ugly but work, for the moment..
        if category == 0:
            if options == 3:
                use_settings  = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Use default settings (y/n): ').lower()

                if use_settings != 'y':
                    Utils.settings_page()

                scrape_cookie = db.scrape_settings['scrape_cookie']

                api = Guilded(__proxies__)
                api.login_from_token(scrape_cookie, True)

                scrapped_teams = api.get_servers(db.scrape_settings['max_scrape']).json()['allTeams']['teams']

                valid = 0
                ttl = len(scrapped_teams)

                for team in scrapped_teams:
                    team_id = team['teamId']
                    members_count = team['measurements']['numMembers']

                    if members_count < db.scrape_settings["min_member"]:
                        continue

                    valid += 1

                    Console.printf(f'({scrape_cookie[:30]}) ({valid}/{ttl}) Scrapped {team_id}, {Fore.GREEN}{Style.BRIGHT}{members_count}/{db.scrape_settings["min_member"]} members{Style.RESET_ALL}.')

                    if db.scrape_settings['join_main']:
                        resp = api.join_team(team_id).status_code

                        if resp == 200:
                            Console.printf(f'({scrape_cookie[:30]}) Success join {team_id}.')
                        else:
                            Console.printf(f'({Fore.LIGHTRED_EX}{scrape_cookie[:30]}) Join failed {team_id}.')

                    with open('./data/scraped_teams.txt', 'a+') as f:
                        f.write(f'{team_id}\n')
            else:

                guild_id      = None
                item          = None

                use_settings  = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Use default settings (y/n): ').lower()

                if use_settings != 'y':
                    Utils.settings_page()

                scrape_cookie = db.scrape_settings['scrape_cookie']
                scrape_default_pfp = db.scrape_settings['scrape_default_pfp']
                with_role_only = db.scrape_settings['with_role_only']
                scrape_online = db.scrape_settings['scrape_online']

                api = Guilded(__proxies__)
                api.login_from_token(scrape_cookie)

                Utils.get_teams()

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
                                    
                                    # kek we won't dm the bots :c
                                    if member['id'] not in db.accounts_ids:
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
            threads = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))
            
            if options == 1:
                Utils.get_teams()
            
            invite = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} InviteCode/TeamID: ')

            Utils.join_accounts(invite, options, threads, db)

        if category == 2:
            threads   = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))

            if options == 0:
                message   = open('./data/message.txt', 'r+', encoding='utf-8', errors='ignore').read()
                Utils.get_teams()

                guild_id = input(f'\n{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} TeamID: ')

                db.ids = list(set(open('./data/id.txt').read().splitlines()))
                db.locked_dm = list(set(open('./data/locked_dm.txt').read().splitlines()))
                db.sent_dm = 0
                db.error_dm = 0
                db.locked = 0

                for uuid in db.ids:
                    if uuid in db.sent:
                        db.ids.remove(uuid)

                Utils.mass_dm(message, threads, db)

            if options == 1:
                message = input(f'\n{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Message: ')
                dm_id = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} UserID: ')
                dm_number = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} NumberOfDms / tokens: '))

                for _ in range(dm_number*len(db.accounts)):
                    db.ids.append(dm_id)
                
                Utils.mass_dm(message, threads, db, True)
            
            if options == 2:
                message = input(f'\n{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Message: ')
                chan_url = input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} ChannelUrl: ')
                
                guild_id = chan_url.split('/channels/')[1].split('/chat')[0]

                # https://www.guilded.gg/fthshshegdsfsds-Comets/groups/3yq59lr3/channels/ceeaf9f8-f4fa-4980-913f-bbda8de02e6e/chat
                # https://www.guilded.gg/i/k1b8rxyp?cid=ceeaf9f8-f4fa-4980-913f-bbda8de02e6e&intent=chat
                #guild_id = chan_url.split('?cid=')[1].split('&intent=chat')[0]
                
                #chan_id  = chan_url.split('/channels/')[1].split('/chat')[0]
                
                Utils.channel_spam(message, guild_id, threads, db)

        if category == 3:
            if options == 0:
                pfp = list(set(open('./data/profilePicture.txt', 'r+').read().splitlines()))

                if not pfp:
                    Console.printf(f'{Style.RESET_ALL}{Fore.RED}*~>{Fore.RESET}  Please put provide pfp link in {Style.BRIGHT}profilePicture.txt{Style.RESET_ALL}.')
                else:
                    threads   = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))
                    Utils.change_pfp(pfp, threads, db)
            
            if options == 2:
                threads   = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))
                Utils.set_online(threads, db)
            
            if options == 3:
                threads   = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))
                Utils.set_status(threads, db)
            
            if options == 4:
                threads   = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))
                Utils.set_bio(threads, db)
            
            if options == 5:
                pfp = list(set(open('./data/profilePicture.txt', 'r+').read().splitlines()))

                if not pfp:
                    Console.printf(f'{Style.RESET_ALL}{Fore.RED}*~>{Fore.RESET}  Please put provide pfp link in {Style.BRIGHT}profilePicture.txt{Style.RESET_ALL}.')
                else:
                    threads   = int(input(f'{Style.RESET_ALL}{Fore.YELLOW}>{Fore.RESET} Max threads: '))
                    Utils.change_pfp(pfp, threads, db)
                    Utils.set_bio(threads, db)
                    Utils.set_status(threads, db)
                    Utils.set_online(threads, db)
        
        if category == 4:
            if options == 0:
                Utils.settings_page()
            
            if options == 1:
                Utils.proxy_settings_page()
            
            if options == 2:
                new_db = Data()
                db = new_db
                
                __proxies__ = Utils.load_proxies()
                Utils.load_accounts(db)