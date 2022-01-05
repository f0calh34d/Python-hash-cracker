import hashlib
import argparse
import os
from termcolor import cprint

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--hash", required=True, help="The hash to crack.")
    parser.add_argument("-t", "--type", required=True, help="The type of the hash. This are the available type of hashes: SHA-1, SHA-3_224, SHA-3_256, SHA-3_384, SHA-3_512, SHA-256, SHA-512, MD5")
    parser.add_argument("-w", "--wordlist", required=True, help="You need to be in the same path as the wordlist.")
    args = parser.parse_args()
    return args

def get_hash_types():
    args = parse_args()
    if args.type == "SHA-1":
        hash_type = hashlib.sha1
    elif args.type == "SHA-3_224":
        hash_type = hashlib.sha3_224
    elif args.type == "SHA-3_256":
        hash_type = hashlib.sha3_256
    elif args.type == "SHA-3_384":
        hash_type = hashlib.sha3_384
    elif args.type == "SHA-3_512":
        hash_type = hashlib.sha3_512
    elif args.type == "SHA-256":
        hash_type = hashlib.sha256
    elif args.type == "SHA-512":
        hash_type = hashlib.sha512
    elif args.type == "MD5":
        hash_type = hashlib.md5
    else:
        return False
    return hash_type

def get_os():
    os_name = os.name
    if os_name == "posix":
        return "GNU/Linux"
    elif os_name == "nt":
        return "Windows"
    else:
        return "Unknown"

def print_info():
    os = get_os()
    print(f"[INFO] Running on {os}")
    print("[INFO] Python Hash Cracker v1")

class HashCracker:
    def __init__(self):
        self.args = parse_args()
        self.hash_type = get_hash_types()
        self.info = print_info()
        self.tried_words = 0

    def main(self):
        if self.hash_type:
            print(self.info)
            print("[+] Started hash cracker")
            try:
                with open(self.args.wordlist, "r", errors="replace") as f:
                    for line in f:
                            plaintext = line.strip()
                            encoded_line = plaintext.encode()
                            hashed_line = self.hash_type(encoded_line).hexdigest()
                            if hashed_line == self.args.hash:
                                cprint(f"[+] Hash found: {plaintext}", "green")
                                print(f"[FINISH INFO] {self.tried_words} words were tried.")
                                break
                            self.tried_words += 1
            except FileNotFoundError:
                cprint("[-] You entered a non valid file.", "red")
                cprint("[-] Hash cracker stopped", "red")
        else:
            cprint("[-] Hash type not valid", "red")
            cprint("[-] Hash cracker stopped", "red")

hashcracker = HashCracker()
hashcracker.main()
