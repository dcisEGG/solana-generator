import base58
from solders.keypair import Keypair
import csv
from tqdm import tqdm
import time

def get_search_pattern():
    pattern_type = input("find pattern in begin (1) or end (2) wallet address? (1/2): ")
    pattern = input("enter patern (not bigger than 4 symbol) (default 'gg'): ").strip()
    
    if not pattern:
        pattern = "gg"
    
    return pattern, pattern_type == "1"

def generate_wallet():
    account = Keypair()
    private_key = base58.b58encode(account.secret() + base58.b58decode(str(account.pubkey()))).decode('utf-8')
    wallet_address = str(account.pubkey())
    return wallet_address, private_key

def main():
    pattern, is_prefix = get_search_pattern()
    print(f"\nFinc Wallet with {'prefix' if is_prefix else 'sufix'}: {pattern}")
    
    with open("wallets.csv", 'w', newline='') as csvfile_all, \
         open("filtered_wallets.csv", 'w', newline='') as csvfile_filtered:
        
        csv_writer_all = csv.writer(csvfile_all)
        csv_writer_filtered = csv.writer(csvfile_filtered)
        
        headers = ["WALLET", "PRIVATE KEY"]
        csv_writer_all.writerow(headers)
        csv_writer_filtered.writerow(headers)
        
        attempts = 0
        found = False
        
        # progress bar
        pbar = tqdm(desc="wallet generation", unit=" wallets")
        
        while not found:
            wallet_address, private_key = generate_wallet()
            attempts += 1
            
            csv_writer_all.writerow([wallet_address, private_key])
            
            # check pattern(wallet)
            if (is_prefix and wallet_address.startswith(pattern)) or \
               (not is_prefix and wallet_address.endswith(pattern)):
                csv_writer_filtered.writerow([wallet_address, private_key])
                found = True
                print(f"\nFind Correct wallet ! after {attempts}attempts !")
                print(f"address: {wallet_address}")
                print(f"private key: {private_key}")
            
            # refresh progress bar every 100 attempts 
            if attempts % 100 == 0:
                pbar.update(100)
        
        pbar.close()

if __name__ == "__main__":
    main()