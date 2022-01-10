import hashlib
import argparse
import os
from typing import List, Optional
from termcolor import cprint
from hashlib import algorithms_available

__VERSION__ = 1.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H", "--hash",
        required=True,
        help="The hash to crack."
    )
    parser.add_argument(
        "-t", "--type",
        required=True,
        choices=algorithms_available,
        help=f"The type of the hash. These are the available types of hashes: {algorithms_available}"
    )
    parser.add_argument(
        "-w", "--wordlist",
        required=True,
        help="Path to wordlist.")
    return parser.parse_args()


class HashCracker:
    os_type = {
        'posix': 'GNU/Linux',
        'nt': 'Windows'
    }

    def __init__(self, wordlist: str) -> None:
        self.wordlist = wordlist

    def crack(self, digest: str, hash_type: str) -> Optional[str]:
        words: List[str] = []
        if hash_type in algorithms_available:
            print(
                f'[INFO] Running on {self.os_type.get(os.name, "Unknown")}\n'
                f'[INFO] Python Hash Cracker v{__VERSION__}'
            )
            print("[+] Started hash cracker")
            try:
                with open(self.wordlist, "r", errors="replace") as f:
                    for line in f:
                        words.append(line.strip())
            except FileNotFoundError:
                cprint("[-] You entered a non valid file.", "red")
                cprint("[-] Hash cracker stopped", "red")

            for n, word in enumerate(words):
                hashed_word = hashlib.new(
                    hash_type, data=word.encode()).hexdigest()

                if hashed_word == digest:
                    result = word
                    cprint(f"[+] Hash found: {result}", "green")
                    print(f"[FINISH INFO] {n} words were tried.")
                    return result

        else:
            cprint("[-] Hash type not valid", "red")
            cprint("[-] Hash cracker stopped", "red")


def main():
    args = parse_args()
    hashcracker = HashCracker(wordlist=args.wordlist)
    hashcracker.crack(digest=args.hash, hash_type=args.type)


if __name__ == '__main__':
    main()
