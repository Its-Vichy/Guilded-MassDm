from colorama import Fore, init, Style; init()
import threading, os, json, random

__lock__, __config__, __version__ = threading.Lock(), json.load(open('./settings/config.json')), '0.0.6'


class Console:
    @staticmethod
    def print_logo():
        os.system(f'cls && title G-MassDM - {__version__}' if os.name == 'nt' else 'clear')
        color = random.choice([Fore.LIGHTMAGENTA_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.YELLOW, Fore.CYAN, Fore.BLUE, Fore.MAGENTA])

        print(f'''
 {color}  ____ {Fore.LIGHTWHITE_EX}    __  __              {color} ____  __  __ {Fore.LIGHTWHITE_EX}
 {color} / ___|{Fore.LIGHTWHITE_EX}   |  \/  | __ _ ___ ___{color}|  _ \|  \/  |{Fore.LIGHTWHITE_EX}
 {color}| |  _ {Fore.LIGHTWHITE_EX}___| |\/| |/ _` / __/ __{color}| | | | |\/| |{Fore.LIGHTWHITE_EX}
 {color}| |_| |{Fore.LIGHTWHITE_EX}___| |  | | (_| \__ \__ \\{color} |_| | |  | |{Fore.LIGHTWHITE_EX}
 {color} \____|{Fore.LIGHTWHITE_EX}   |_|  |_|\__,_|___/___/{color}____/|_|  |_|{Fore.LIGHTWHITE_EX} {Style.BRIGHT}github.com/its-vichy{Style.RESET_ALL}
        
        ''')

    @staticmethod
    def printf(content: str):
        __lock__.acquire()
        print(content.replace('(', f'({Fore.LIGHTBLUE_EX}').replace(')', f'{Fore.RESET})'))
        __lock__.release()

    @staticmethod
    def debug(content: str):
        if __config__['debug']:
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
            - [{Fore.LIGHTBLUE_EX}3{Fore.LIGHTWHITE_EX}] Server Guild.
            
        [{Fore.YELLOW}1{Fore.LIGHTWHITE_EX}] Joiner:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Join guild.
            - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Join team.
            
        [{Fore.YELLOW}2{Fore.LIGHTWHITE_EX}] MassDM:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Mass DM guild.
            - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Single Mass DM.
            - [{Fore.LIGHTBLUE_EX}2{Fore.LIGHTWHITE_EX}] Channel spammer.
        
        [{Fore.YELLOW}3{Fore.LIGHTWHITE_EX}] Mass Actions:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Mass pfp changer.
            - [{Fore.LIGHTBLUE_EX}2{Fore.LIGHTWHITE_EX}] Mass Onliner.
            - [{Fore.LIGHTBLUE_EX}3{Fore.LIGHTWHITE_EX}] Mass status changer.
            - [{Fore.LIGHTBLUE_EX}4{Fore.LIGHTWHITE_EX}] Mass bio changer.
            - [{Fore.LIGHTBLUE_EX}5{Fore.LIGHTWHITE_EX}] Mass spoof (bio+status+pfp+online).
        
        [{Fore.YELLOW}4{Fore.LIGHTWHITE_EX}] Util:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Edit Proxy config.
            - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Edit Scrape config.
            - [{Fore.LIGHTBLUE_EX}2{Fore.LIGHTWHITE_EX}] Reload files (id, proxies, cookies etc...).
        ''')
