# Copyrith 2016 - written by Rojo Ambinina

#  This code is only for generating compressed and uncompressed bitcoins addresses with their balances, and also displays the private keys at the same time.
#  The algorithm generates bitcoin addresses until it finds a non-zero balance and stores it in a text file "Lottery_BTC.txt"

#  Using it is easy, you only have to type the command below to install the bitcoin module:
#  pip install bitcoin

#  Then just go to the folder containing the file "btc-balance.py" to run the algorithm:
#  py btc-balance.py

#  This code is only for example study and does not run too fast to avoid spamming Blockchain, but you can modify it by adding the multiprocessing module.


import json, requests
import time
import sys
import bitcoin
from bitcoin import *

    
toolbar_width = 40
btc = 20
n = 1
count = 1
while True:
    try:
        if count < 21:
            # Generate a random private key
            blockcipher = random_key()
            my_public_key1 = privtopub(blockcipher)
            blockchain = random_key()
            my_public_key2 = privtopub(blockchain)
            private_key = random_key()
            my_private_key3 = private_key
            my_public_key3 = privtopub(private_key)
            my_multi_sig = mk_multisig_script(blockcipher,
            blockchain, private_key, 2,3)
            my_multi_address = scriptaddr(my_multi_sig)
            multi_block = my_multi_address
            valid_private_key = False
            while not valid_private_key:
                private_key = bitcoin.random_key()
                decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
                valid_private_key =  0 < decoded_private_key < bitcoin.N
            wif_encoded_private_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
            compressed_private_key = private_key + '01'
            wif_compressed_private_key = bitcoin.encode_privkey(bitcoin.decode_privkey(compressed_private_key, 'hex'), 'wif')
            public_key = bitcoin.fast_multiply(bitcoin.G, decoded_private_key)
            hex_encoded_public_key = bitcoin.encode_pubkey(public_key,'hex')
            (public_key_x, public_key_y) = public_key
            if (public_key_y % 2) == 0:
                compressed_prefix = '02'
            else:
                compressed_prefix = '03'
            hex_compressed_public_key = compressed_prefix + bitcoin.encode(public_key_x, 16)
            uncompressed_block = requests.get('https://blockchain.info/balance?active='+ str(bitcoin.pubkey_to_address(public_key)))
            uncompressed_json = json.loads(uncompressed_block.text)[bitcoin.pubkey_to_address(public_key)]
            compressed_block = requests.get('https://blockchain.info/balance?active='+ str(bitcoin.pubkey_to_address(hex_compressed_public_key)))
            compressed_json = json.loads(compressed_block.text)[bitcoin.pubkey_to_address(hex_compressed_public_key)]
            multi_block = requests.get('https://blockchain.info/balance?active='+ str(my_multi_address))
            multi_json = json.loads(multi_block.text)[my_multi_address]
            if int(uncompressed_json["final_balance"]) > 0 or int(compressed_json["final_balance"]) > 0 or int(multi_json["final_balance"]) > 0:
                balance = open("Lottery_BTC.txt","a+")
                balance.write(" Uncompressed Private Key\t\t:  " + wif_encoded_private_key +  "\n Compressed Private key\t\t:  " + wif_compressed_private_key + "\n Uncompressed Bitcoin Address\t:  " + bitcoin.pubkey_to_address(public_key) + " \t\t\t\t\t\t Uncompressed Balance: " + str(int(uncompressed_json["final_balance"])) + "\n Compressed Bitcoin Address\t\t:  " + bitcoin.pubkey_to_address(hex_compressed_public_key) + "\t\t\t\t\t\t Compressed Balance: " + str(int(compressed_json["final_balance"])) + "\n Multi BTC Address\t\t\t:  " + str(my_multi_address) + "\n Third Private Key\t\t\t:  " + str(my_private_key3) + "\t\t\t Third Balance: " + str(int(multi_json["final_balance"])) + "\n Private Key Hexadecimal\t\t:  " + str(private_key) + "\n\n")
                balance.close()
                print("\nYou have just rung the bell of BTC Lottery !!!")
            else:
                print('\t-------------------------------------------------------------------------------------------------------\n')
                print("\t" + str(count) + "\t Private Key (WIF-Uncompressed) \t: ", wif_encoded_private_key)
                print("\t\t Private Key (WIF-Compressed) \t\t: ", wif_compressed_private_key + "\n")
                print("\t\t Uncompressed Bitcoin Address \t\t: ", bitcoin.pubkey_to_address(public_key))
                print("\t\t Final Balance \t\t\t\t:  " + str(int(uncompressed_json["final_balance"])) + "\n")
                print("\t\t Compressed Bitcoin Address \t\t: ", bitcoin.pubkey_to_address(hex_compressed_public_key))
                print("\t\t Final Balance \t\t\t\t:  " + str(int(compressed_json["final_balance"])) + "\n")
                print("\t\t Private Key Hexadecimal \t\t:  " + str(private_key))
                print("\t\t Multiple BTC Address \t\t\t:  " + str(my_multi_address))
                print("\t\t Third Final Balance \t\t\t:  " + str(int(multi_json["final_balance"])) + "\n")
                print("\n \t\t\t\t\t You have no lucky yet !!! \n")
            count += 1
            time.sleep(3)
        else:
            print("\t" + str(n) + " round(s) done, " + str(btc) + " BTC Address have been generated, waiting 60 seconds ... \n")
            btc += 20
            n += 1
            for i in range(toolbar_width):
               time.sleep(2) # do real work here
               # update the bar
               sys.stdout.write(" ")
               sys.stdout.write("|||")
               sys.stdout.flush()
            sys.stdout.write("\n\n")
            print("\t Restarting ... \n")
            time.sleep(5)            
            count = 1
    except:
        print("\t Something went wrong, please wait ...\n")
        time.sleep(15)
        print("\t Error solved, Restarting ... \n")
        count = 1