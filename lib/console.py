from colorama import Fore, init, Style; init()
import threading, os, json

__lock__, __config__ = threading.Lock(), json.load(open('./config.json'))


class Console:
    @staticmethod
    def print_logo():
        os.system('cls && title G-MassDM' if os.name == 'nt' else 'clear')
        print(f'''
 {Fore.YELLOW}  ____ {Fore.LIGHTWHITE_EX}    __  __              {Fore.YELLOW} ____  __  __ {Fore.LIGHTWHITE_EX}
 {Fore.YELLOW} / ___|{Fore.LIGHTWHITE_EX}   |  \/  | __ _ ___ ___{Fore.YELLOW}|  _ \|  \/  |{Fore.LIGHTWHITE_EX}
 {Fore.YELLOW}| |  _ {Fore.LIGHTWHITE_EX}___| |\/| |/ _` / __/ __{Fore.YELLOW}| | | | |\/| |{Fore.LIGHTWHITE_EX}
 {Fore.YELLOW}| |_| |{Fore.LIGHTWHITE_EX}___| |  | | (_| \__ \__ \\{Fore.YELLOW} |_| | |  | |{Fore.LIGHTWHITE_EX}
 {Fore.YELLOW} \____|{Fore.LIGHTWHITE_EX}   |_|  |_|\__,_|___/___/{Fore.YELLOW}____/|_|  |_|{Fore.LIGHTWHITE_EX} {Style.BRIGHT}github.com/its-vichy{Style.RESET_ALL}
        
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
            
        [{Fore.YELLOW}1{Fore.LIGHTWHITE_EX}] Joiner:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Join guild.
            - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Join team.
            
        [{Fore.YELLOW}2{Fore.LIGHTWHITE_EX}] MassDM:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Mass DM guild.
        
        [{Fore.YELLOW}3{Fore.LIGHTWHITE_EX}] Util:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Mass pfp changer.
            - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Config the tool.
        ''')
