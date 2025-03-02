#!/usr/bin/python3
import requests
import time
import os
import subprocess
from config import ENGINES
from utils import random_headers, get_proc_pos
from arguments import parse_arguments
from colorama import init, Fore, Back, Style
from stem import Signal
from stem.control import Controller

# Initialize colorama
init(autoreset=True)

# Function to start Tor and get the SOCKS proxy details
def start_tor():
    # Linux path to the Tor executable
    tor_path = "/usr/bin/tor"
    
    if not os.path.isfile(tor_path):
        print(Fore.RED + f"Tor executable not found at {tor_path}")
        return None, None

    try:
        print(Fore.YELLOW + "Starting Tor...")
        process = subprocess.Popen([tor_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = process.communicate(timeout=20)  # Timeout after 20 seconds
        except subprocess.TimeoutExpired:
            print(Fore.RED + "Tor startup timed out.")
            process.kill()
            return None, None

        if process.returncode != 0:
            print(Fore.RED + f"Tor failed to start: {stderr.decode()}")
            print(Fore.YELLOW + f"Tor output: {stdout.decode()}")
            return None, None
        print(Fore.GREEN + "Tor started successfully.")
        return "127.0.0.1", 9050  # Local SOCKS proxy
    except Exception as e:
        print(Fore.RED + f"Failed to start Tor: {e}")
        return None, None

# Function to switch Tor identity
def switch_tor_identity():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            print(Fore.GREEN + "Tor identity switched.")
    except Exception as e:
        print(Fore.RED + f"Failed to switch Tor identity: {e}")

# Function to make an HTTP request through the Tor network
def make_request(url, proxies):
    try:
        response = requests.get(url, proxies=proxies, headers=random_headers())
        return response
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Request failed: {e}")
        return 

def main():
    # ASCII Art

    ascii_art = f'''
{Fore.RED}⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⢟⣵⢿⢛⣿⣿⣿⣿⣿⣿⣯⣞⣿⣿⣿⣤⣀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣽
⣿⣿⣿⣿⣯⢵⣪⣷⣿⣿⣿⣿⣿⣟⣵⢯⣿⣿⣳⣻⣿⣯⡆⢻⣿⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣹⢾⣿⣿
⣟⢿⣻⣯⣷⣿⣿⣿⣿⡿⣿⣿⣟⣾⢏⣿⣿⢧⡏⣿⣿⣼⣿⣄⡙⠿⣮⣟⡿⠿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣯⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣵⣙⢿
⣿⣷⣿⣽⣟⣻⣿⡿⣫⣾⣿⡿⣾⠋⣼⢿⠃⣼⢹⣿⠋⣿⣿⣿⣿⣷⣶⣶⣿⢿⣶⣶⣞⣿⣿⣿⣿⣿⣿⣿⣷⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣹⣿
⣿⣿⣿⣿⣿⣿⢯⣾⣿⡿⠿⢷⠁⠀⣿⠇⠀⠁⢸⠃⠀⣿⣿⣿⣿⣿⢹⣿⣿⡏⢿⣿⣿⣞⠻⣿⢿⣿⡟⢿⣿⣷⠀⠉⠻⣿⣿⣿⣿⣿⣟⡿⣿⣷⢿
⣿⣿⣿⣿⣿⣏⡿⠋⠁⠀⠀⠀⠀⠀⡏⠀⠀⠀⠈⠀⠀⢿⡇⢻⣿⠹⡌⢻⣿⣷⠀⠋⠻⢿⠀⠈⠂⠙⢿⠀⠈⢿⡇⠀⠀⠘⠏⠻⣿⣿⣿⣟⣷⣽⡛
{Fore.BLUE}⣿⣿⣿⣿⣿⠉⠀⣀⣤⠂⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠸⠀⠈⢿⠀⠁⠀⠹⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠁⠀⠀⠀⠀⠀⠈⢯⢛⡿⣯⡻⣿
⣿⣿⣿⣿⣟⣴⣾⣿⠃⣠⡴⠀⠀⠀⠀⢰⣸⡎⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⢈⢟⣿⣷⣶⣾
⣿⣿⣿⣿⣿⣿⣿⣇⣴⣿⠇⠀⠀⠀⠀⠸⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⢀⠀⢀⣀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⢸⣾⡄⠀⠀⠀⢸⣮⢹⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢀⣠⣤⣾⠀⢀⣿⣿⡻⢶⣦⣮⣧⡀⠘⣦⡘⡟⣨⡄⠀⠀⠀⠀⢠⣿⣏⣦⡆⠀⢠⠀⠀⢈⣿⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⡄⣿⣿⣿⢿⣶⣶⣿⢟⣿⣖⣿⣷⣿⣿⣻⠶⣤⣤⣶⠟⣿⣿⢿⡇⢰⠏⠀⠀⠸⠋⠀⢀⠀⠀⠈⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡏⣼⣿⣷⡀⣿⣿⣿⣿⣿⣿⣿⣻⠀⠀⠀⢠⣪⡽⣿⣿⠧⠿⡶⠞⠃⠀⠀⡀⢸⣿⣶⣶⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡲⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⢄⠀⣰⣵⣦⣆⠟⠁⠀⠀⠀⠀⢠⡎⣸⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿
{Fore.MAGENTA}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡻⣿⣿⣿⣟⣻⢿⣿⣿⣿⣷⣾⢸⣿⠏⠞⠁⠀⠀⠠⡞⣴⣰⣿⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠙⢿⣦⣉⣿⣿⣿⣿⡿⠏⠚⠉⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⠀⠀⠙⠿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣯⣶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣷⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣽⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⢿⣿⣾⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⡿⢹⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡰⡵⣠⣿⣿⣿⣷⣮⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡟⠁⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣲⠟⢫⠞⣽⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⡿⣿⣿⣿⣿⣿⣿
{Fore.RED}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠃⠉⠀⠀⠀⣼⢿⣿⣿⣧⣿⢟⣵⣿⣿⣿⣿⣿⣞⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣫⣿⠀⣾⣿⣿⣿⠀⠀⠀⠀⠀⠀⣠⡾⣃⢤⣾⣡⠊⠀⣸⣟⠏⣿⣿⡿⣣⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⢀⣿⣿⣿⣿⠀⠀⠀⠀⣠⣾⣿⢟⣡⣾⣿⡏⠀⡸⡿⣼⣵⣿⡿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⣿⣿⢸⣿⡏⣹⣿⠀⠀⣠⣾⣿⡿⣻⣿⣿⣟⡽⠀⢰⣡⢁⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    '''
    time.sleep(1)
    print(ascii_art)
    time.sleep(3)
    print("\n################\n")
    print("GG GET SCRAPED\n")
    print("Made by Th3Cha1rman\n")
    print("################")

    
  # Start Tor and get the SOCKS proxy
    proxy_host, proxy_port = start_tor()
    if not proxy_host:
        print(Fore.RED + "Exiting due to Tor failure.")
        return

    proxies = {
        "http": f"socks5://{proxy_host}:{proxy_port}",
        "https": f"socks5://{proxy_host}:{proxy_port}"
    }

    # Request example using the Tor proxy
    url = "http://httpbin.org/ip"  # Example URL to check IP through Tor
    response = make_request(url, proxies)

    if response:
        print(Fore.GREEN + f"Response: {response.json()}")

    # Allow switching Tor identity every 5 minutes
    while True:
        time.sleep(300)  # Sleep for 5 minutes
        switch_tor_identity()

if __name__ == "__main__":
    main()