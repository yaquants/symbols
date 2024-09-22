import requests
import time
import os

def fetch_symbols(categories, processed_file='processed_categories.txt'):
    all_symbols = []
    processed_categories = load_processed_categories(processed_file)

    for category in categories:
        if category in processed_categories:
            print(f"Skipping category '{category}', already processed.")
            continue

        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category={category}" 
        retry_attempts = 3
        for attempt in range(retry_attempts):
            try:
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    symbols = [coin['symbol'].upper() + 'USD' for coin in data]
                    all_symbols.extend(symbols)
                    print(f"Fetching symbols for category '{category}' successful.")
                    
                    # Mark this category as processed
                    save_processed_category(category, processed_file)
                    break
                
                elif response.status_code == 429:
                    print(f"Rate limit hit. Waiting before retrying... (Category: {category})")
                    time.sleep(60)  # Adjust this wait time based on rate limits
                else:
                    print(f"Failed to fetch symbols for category '{category}', status code: {response.status_code}")
                    break

            except Exception as e:
                print(f"Attempt {attempt + 1} failed for category '{category}': {e}")
                time.sleep(2)

    return all_symbols

def send_to_server(symbols):
    url = 'http://localhost:5000/receive_symbols'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json={'symbols': symbols}, headers=headers)
    if response.status_code == 200:
        print("Symbols sent successfully")
    else:
        print(f"Failed to send symbols, status code: {response.status_code}")

# Functions to load and save processed categories
def load_processed_categories(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        return f.read().splitlines()

def save_processed_category(category, filename):
    with open(filename, 'a') as f:
        f.write(category + '\n')

# List of all categories
all_categories = [
    'layer-1', 'depin', 'proof-of-work-pow', 'proof-of-stake-pos', 'meme-token', 'dog-themed-coins', 
    'eth-2-0-staking', 'non-fungible-tokens-nft', 'governance', 'artificial-intelligence', 
    'infrastructure', 'layer-2', 'zero-knowledge-zk', 'storage', 'oracle', 'bitcoin-fork', 
    'restaking', 'rollup', 'metaverse', 'privacy-coins', 'layer-0-l0', 'solana-meme-coins', 
    'data-availability', 'internet-of-things-iot', 'frog-themed-coins', 'ai-agents', 
    'superchain-ecosystem', 'bitcoin-layer-2', 'bridge-governance-tokens', 'modular-blockchain', 
    'cat-themed-coins', 'cross-chain-communication', 'analytics', 'identity', 'wallets', 'masternodes'
]

# Fetch symbols and send to server
symbols = fetch_symbols(all_categories)
send_to_server(symbols)
