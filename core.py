import traceback
import json
from valclient.client import Client
from colorama import init, Fore, Style

init(autoreset=True)

banner = r"""
                    ..
                   ( '`<
                    )(
             (  ----'  '.
             (         ;
              (_______,' 
^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^^~^~^
"""



allowed_regions = ['na', 'eu', 'latam', 'br', 'ap', 'kr', 'pbe']

main = f"{Style.BRIGHT}{Fore.MAGENTA} Valorant Agent Locker by quarterwire."
req_region = f"{Fore.RED} Enter Region (EU/NA) : "
req_agent = f"{Fore.RED} Agent (e.g Jett) : "
err_agent = f"{Fore.YELLOW} Invalid agent name."
err_region = f"{Fore.YELLOW} Region not matching with any {'/'.join([r.upper() for r in allowed_regions])}."
waiting = f"{Fore.GREEN} Waiting for Agent Select screen."
game_found =f'{Fore.GREEN} Agent Selection was found.'


print(f"{Style.BRIGHT} {Fore.GREEN} {banner}")
print(main)

region = input(f"{req_region}").lower()

while region not in allowed_regions:
    print(f"{err_region}")
    region = input(f"{req_region}").lower()
    
client = Client(region = region)
client.activate()
valid = False
agents = {}
past_matches = []

with open("agentIds.json", "r") as f:
        agents = json.load(f)
        
while not valid:
    try:
        pref_agent = input(f"{req_agent}").lower()
        if pref_agent in agents["agents"].keys():
            valid = True
        else:
            print(f"{err_agent}")
    except Exception:
        print(f'{traceback.format_exc()}')
        
print(f"{Fore.YELLOW} Waiting for Agent Selection")
while True:
    try:
        sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
        if sessionState == "PREGAME" and client.pregame_fetch_match()['ID'] not in past_matches:
            print(game_found)
            client.pregame_select_character(agents['agents'][pref_agent])
            client.pregame_lock_character(agents['agents'][pref_agent])
            past_matches.append(client.pregame_fetch_match()['ID'])
            print(f"{Fore.LIGHTWHITE_EX}{pref_agent.capitalize()} Locked Successfully")
    except Exception:
        pass



        
        

