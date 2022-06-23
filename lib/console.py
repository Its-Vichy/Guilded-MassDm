import threading, json, random, re, httpx, os
from colorama import Fore, init; init()

__lock__, __config__ = threading.Lock(), json.load(open('./settings/config.json'))

users = re.findall(r'<div class="visits" title="Unique visits to this paste">\n(.+)<\/div>', httpx.get('https://pastebin.com/nkT1D7iJ').text)[0].strip()
color = random.choice([Fore.LIGHTGREEN_EX, Fore.YELLOW, Fore.MAGENTA])

class Console:
    @staticmethod
    def print_logo():
        # Nice idea (https://github.com/V4NSH4J/discord-mass-DM-GO/blob/main/utilities/misc.go)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f''' {color}  ____ {Fore.LIGHTWHITE_EX}    __  __              {color} ____  __  __ {Fore.LIGHTWHITE_EX}
 {color} / ___|{Fore.LIGHTWHITE_EX}   |  \/  | __ _ ___ ___{color}|  _ \|  \/  |{Fore.LIGHTWHITE_EX}
 {color}| |  _ {Fore.LIGHTWHITE_EX}___| |\/| |/ _` / __/ __{color}| | | | |\/| |{Fore.LIGHTWHITE_EX}
 {color}| |_| |{Fore.LIGHTWHITE_EX}___| |  | | (_| \__ \__ \\{color} |_| | |  | |{Fore.LIGHTWHITE_EX} Users: {color}{users}{Fore.RESET}
 {color} \____|{Fore.LIGHTWHITE_EX}   |_|  |_|\__,_|___/___/{color}____/|_|  |_|{Fore.LIGHTWHITE_EX} github.com/{color}its-vichy{Fore.RESET}
        
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
        print(f'''  {Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX} Options{Fore.LIGHTBLUE_EX}:{Fore.LIGHTWHITE_EX}
        [{color}0{Fore.LIGHTWHITE_EX}] Scraper:                          [{color}1{Fore.LIGHTWHITE_EX}] Joiner/Leaver:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Scrape id.                    - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Join guild.
            - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Scrape avatars.               - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Join team.
            - [{Fore.LIGHTBLUE_EX}2{Fore.LIGHTWHITE_EX}] Scrape usernames.             - [{Fore.LIGHTBLUE_EX}2{Fore.LIGHTWHITE_EX}] Leaver.
            - [{Fore.LIGHTBLUE_EX}3{Fore.LIGHTWHITE_EX}] Server Guild.                 - [{Fore.LIGHTBLUE_EX}3{Fore.LIGHTWHITE_EX}] Join/Leave spammer.
            
            
        [{color}2{Fore.LIGHTWHITE_EX}] MassDM:                            [{color}4{Fore.LIGHTWHITE_EX}] Util:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Mass DM guild.                 - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Edit Scrape config.
            - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Single Mass DM.                - [{Fore.LIGHTBLUE_EX}1{Fore.LIGHTWHITE_EX}] Edit Proxy config.
            - [{Fore.LIGHTBLUE_EX}2{Fore.LIGHTWHITE_EX}] Channel spammer.               - [{Fore.LIGHTBLUE_EX}2{Fore.LIGHTWHITE_EX}] Reload files (id, proxies, cookies etc...).
                                                                                
        [{color}3{Fore.LIGHTWHITE_EX}] Mass Actions:
            - [{Fore.LIGHTBLUE_EX}0{Fore.LIGHTWHITE_EX}] Mass pfp changer.
            - [{Fore.LIGHTBLUE_EX}2{Fore.LIGHTWHITE_EX}] Mass Onliner.
            - [{Fore.LIGHTBLUE_EX}3{Fore.LIGHTWHITE_EX}] Mass status changer.
            - [{Fore.LIGHTBLUE_EX}4{Fore.LIGHTWHITE_EX}] Mass bio changer.
            - [{Fore.LIGHTBLUE_EX}5{Fore.LIGHTWHITE_EX}] Mass spoof (A.I.O).
        ''')