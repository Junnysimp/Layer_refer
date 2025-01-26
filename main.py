import ssl
import certifi
import requests
import json
import random
import time
import string
import subprocess
from web3 import Web3
from eth_account import Account
from colorama import init, Fore, Style

# Suppress SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# Initialize colorama
init()

# Custom Banner
print(Fore.GREEN + "╔══════════════════════════════════╗")
print(Fore.GREEN + "║  Layer Referral Automation       ║")
print(Fore.GREEN + "║  Automated Wallet Creation       ║")
print(Fore.GREEN + "║  and Mining Script               ║")
print(Fore.GREEN + "╚══════════════════════════════════╝" + Style.RESET_ALL)

def generate_wallet():
    """Generate a new Ethereum wallet with private key and mnemonic phrase."""
    Account.enable_unaudited_hdwallet_features()
    mnemonic = Account.create_with_mnemonic()
    account = Account.from_mnemonic(mnemonic[1])
    return {
        "address": account.address,
        "private_key": account._private_key.hex(),
        "mnemonic": mnemonic[1]
    }

def save_wallet(wallet):
    """Save the wallet to wallets.json."""
    try:
        with open("wallets.json", "r") as file:
            wallets = json.load(file)
    except FileNotFoundError:
        wallets = []

    wallets.append(wallet)
    with open("wallets.json", "w") as file:
        json.dump(wallets, file, indent=4)

def start_mining(wallet_address):
    """Start a mining process for the given wallet address."""
    mining_command = f"./start_mining.sh {wallet_address}"
    try:
        subprocess.run(mining_command, shell=True, check=True)
        print(Fore.GREEN + f"Mining started for wallet: {wallet_address}" + Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Failed to start mining for wallet {wallet_address}: {e}" + Style.RESET_ALL)

# Hardcoded referral code
referral_code = "6EIInbwa"
url = f"https://referral.layeredge.io/api/referral/register-wallet/{referral_code}"

headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://dashboard.layeredge.io',
    'Referer': 'https://dashboard.layeredge.io/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

# Counter for wallet numbering
wallet_counter = 1

while True:
    # Generate a new Ethereum wallet
    wallet = generate_wallet()
    payload = json.dumps({
        "walletAddress": wallet["address"]
    })

    try:
        # Register the wallet with the referral system
        response = requests.post(url, headers=headers, data=payload, verify=False)
        response_data = response.json()

        # Display the response in a structured format
        print(Fore.GREEN + "╔══════════════════════════════════╗")
        print(Fore.GREEN + f"║ Wallet {wallet_counter} Created Successfully! ║")
        print(Fore.GREEN + "╠══════════════════════════════════╣")
        print(Fore.GREEN + f"║ Wallet Address: {wallet['address']}")
        print(Fore.GREEN + f"║ Private Key: {wallet['private_key']}")
        print(Fore.GREEN + f"║ Mnemonic Phrase: {wallet['mnemonic']}")
        print(Fore.GREEN + f"║ Referral Code: {response_data['data']['referralCode']}")
        print(Fore.GREEN + f"║ Total Points: {response_data['data']['totalPoints']}")
        print(Fore.GREEN + f"║ Node Points: {response_data['data']['nodePoints']}")
        print(Fore.GREEN + f"║ Last Claimed: {response_data['data']['lastClaimed'] or 'N/A'}")
        print(Fore.GREEN + f"║ Created At: {response_data['data']['createdAt']}")
        print(Fore.GREEN + "╚══════════════════════════════════╝" + Style.RESET_ALL)

        # Save the wallet to wallets.json
        save_wallet(wallet)

        # Start mining for the new wallet
        start_mining(wallet["address"])

        # Increment the wallet counter
        wallet_counter += 1
    except Exception as e:
        # Handle errors
        print(Fore.RED + f"Error occurred: {str(e)}" + Style.RESET_ALL)

    # Add a random delay between requests
    delay = random.randint(60, 100)  # Delay in milliseconds
    print(Fore.GREEN + f"Next request in {delay} milliseconds..." + Style.RESET_ALL)
    time.sleep(delay / 1000)  # Convert milliseconds to seconds for time.sleep()
