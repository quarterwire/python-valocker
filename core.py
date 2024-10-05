import traceback
import json
from valclient.client import Client
from colorama import init, Fore, Style
import subprocess
import time
import os
import shutil

init(autoreset=True)
os.system('cls' if os.name == 'nt' else 'clear')

def print_centre(s, end=None):
    terminal_width = shutil.get_terminal_size().columns
    for line in s.splitlines():
        left_padding = (terminal_width - len(line)) // 2
        print(' ' * left_padding + line, end=end)

def clear_line():
    print("\033[F\033[K", end='')  # Clear only the last printed line

def is_val_running():
    valorant_process = "VALORANT.exe"
    call = 'TASKLIST', '/FI', f'imagename eq {valorant_process}'
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(valorant_process.lower())

def colored_input(cmd_color, input_color, message):
    print_centre(f'{cmd_color} {message}', end='')
    return_input = input(f"{Style.BRIGHT}{input_color}").lower()
    return return_input

banner = """
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
req_region = f"Enter region (EU/NA) : "
req_agent = f"Select your agent (e.g Jett) : "
err_agent = f"{Fore.YELLOW} Invalid agent name."
err_region = f"{Fore.YELLOW} Region not matching with any {'/'.join([r.upper() for r in allowed_regions])}."
waiting = f"{Fore.GREEN} Waiting for agent select screen."
game_found = f'{Fore.GREEN} Agent selection was found.'

print_centre(f"{Style.BRIGHT}{Fore.GREEN}{banner}")
print_centre(main)

# Get the region input
region = colored_input(Fore.BLUE, Fore.WHITE, req_region)
while region not in allowed_regions:
    print_centre(f"{err_region}")
    region = colored_input(Fore.BLUE, Fore.WHITE, req_region)

# Wait for Valorant to start
def wait_for_val():
    last_message = ""
    while not is_val_running():
        current_message = f"{Fore.RED} Valorant is not running."
        if current_message != last_message:
            clear_line()
            print_centre(current_message)
            last_message = current_message
        time.sleep(5)

wait_for_val()

client = Client(region=region)
client.activate()
valid = False
agents = {}
past_matches = []

with open("agentIds.json", "r") as f:
    agents = json.load(f)

# Get the agent input
while not valid:
    try:
        pref_agent = colored_input(Fore.BLUE, Fore.WHITE, req_agent)
        if pref_agent in agents["agents"].keys():
            valid = True
        else:
            print_centre(f"{err_agent}")
    except json.JSONDecodeError:
        print_centre(f"{Fore.RED} Error loading agent data.")
        break
    except Exception:
        print_centre(f'{traceback.format_exc()}')

print_centre(f"{Fore.YELLOW} Waiting for Agent Selection")

# Main loop for agent selection
while True:
    try:
        sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
        if sessionState == "PREGAME" and client.pregame_fetch_match()['ID'] not in past_matches:
            print_centre(game_found)
            client.pregame_select_character(agents['agents'][pref_agent])
            client.pregame_lock_character(agents['agents'][pref_agent])
            past_matches.append(client.pregame_fetch_match()['ID'])
            print_centre(f"{Fore.LIGHTWHITE_EX}{pref_agent.upper()} locked successfully.")
    except KeyboardInterrupt:
        print_centre(f"\n{Fore.YELLOW} Exiting the program.")
        break
    except Exception as e:
        print_centre(f"{Fore.RED} An error occurred: {str(e)}")
 