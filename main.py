from colorama import Fore, init; init()
import os, threading, time, itertools
from lib.scraper import Scrapper
from lib.joiner import Joiner
from lib.data import Data
from lib.Dm import Dm

if __name__ == '__main__':
    data = Data()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'''{Fore.YELLOW}Guilded MassDM version {Fore.LIGHTCYAN_EX}0.0.1{Fore.YELLOW}.{Fore.LIGHTWHITE_EX} - {Fore.YELLOW}Made by github.com/its-vichy{Fore.LIGHTWHITE_EX}

    > Loaded cookies: {Fore.LIGHTCYAN_EX}{len(data.cookies)}{Fore.LIGHTWHITE_EX}

    > Options:
            [{Fore.MAGENTA}0{Fore.LIGHTWHITE_EX}] Scraper:
                - [{Fore.LIGHTMAGENTA_EX}0{Fore.LIGHTWHITE_EX}] Scrape id.
                - [{Fore.LIGHTMAGENTA_EX}1{Fore.LIGHTWHITE_EX}] Scrape avatars.
                - [{Fore.LIGHTMAGENTA_EX}2{Fore.LIGHTWHITE_EX}] Scrape usernames.
            
            [{Fore.MAGENTA}1{Fore.LIGHTWHITE_EX}] Joiner:
                - [{Fore.LIGHTMAGENTA_EX}0{Fore.LIGHTWHITE_EX}] Join guild.
                - [{Fore.LIGHTMAGENTA_EX}1{Fore.LIGHTWHITE_EX}] Join team.
            
            [{Fore.MAGENTA}2{Fore.LIGHTWHITE_EX}] MassDM:
                - [{Fore.LIGHTMAGENTA_EX}0{Fore.LIGHTWHITE_EX}] Mass DM guild.
        ''')

        category = int(input('Category: '))
        options  = int(input('Option: '))

        os.system('cls' if os.name == 'nt' else 'clear')

        if category == 0:
            scrape_cookie = input('Scrape cookie: ')
            guild_id      = input('Guild Id: ')

            scrapper = Scrapper(scrape_cookie)

            if options == 0:
                ids = scrapper.scrape_members_ids(guild_id)

                print(f'[*] Scraped {len(ids)} ids, saving into ids.txt..')

                with open('./data/ids.txt', 'a+') as f:
                    for member in ids:
                        f.write(member.split("\n")[0] + '\n')
                
                input('Sucess, press key to exit...')
            
            if options == 1:
                avatars = scrapper.scrape_avatar(guild_id)

                print(f'[*] Scraped {len(avatars)} avatars, saving into avatars.txt..')

                with open('./data/avatars.txt', 'a+') as f:
                    for pdp in avatars:
                        f.write(pdp.split("\n")[0] + '\n')
                
                input('Sucess, press key to exit...')
            
            if options == 2:
                username = scrapper.scrape_username(guild_id)

                print(f'[*] Scraped {len(username)} usernames, saving into username.txt..')

                with open('./data/username.txt', 'a+') as f:
                    for user in username:
                        f.write(user.split("\n")[0] + '\n')
                
                input('Sucess, press key to exit...')
        
        if category == 1:
            invite  = input('Invite code: ')
            threads  = int(input('threads: '))

            for token in data.cookies:
                while threading.active_count() >= threads:
                    time.sleep(1)
                
                Joiner(token, invite, options).start()
            
            while threading.active_count() != 1:
                time.sleep(1)
        
        if category == 2:
            if options == 0:
                message = input('message: ')
                guild_id = input('guild id: ')
                threads = int(input('threads: '))
                cookies = itertools.cycle(data.cookies)

                for member in list(set(open('./data/ids.txt', 'r+').read().splitlines())):
                    while threading.active_count() >= threads:
                        time.sleep(1)

                    Dm(next(cookies), member.split('\n')[0], message).start()
                
                while threading.active_count() != 1:
                    time.sleep(1)
                
                input('finished..')