# BIP39 mnemonic (seed phrase) generator
# Author: Brian (deathlyface)

import os, sys, hashlib, urllib.request

print("-------------------------------")
print("| BIP39 Seed Phrase Generator |")
print("| Author: Brian (deathlyface) |")
print("-------------------------------")
print()
print("\33[1;37mINFO\33[1;0m: Please verify that you received this code from https://github.com/deathlyface/py-bip39.")
print("\33[1;37mINFO\33[1;0m: By default, this software uses PRNG to get some random bytes. For better security, you can plug in a HRNG/TRNG device.")
print()

if len(sys.argv) != 2 or sys.argv[1] not in ["12", "24"]:
    print("Usage: ")
    print("    python3 {} 12".format(sys.argv[0]))
    print("    python3 {} 24".format(sys.argv[0]))
    exit()

try:
    r = urllib.request.urlopen("http://example.com")
    if r.status:
        print("\33[1;33mWARNING\33[1;0m: You are connected to the internet. We recommend that you run this code offline.\n")
except:
    pass

print("Generating seed phrase with a length of {} words.\n".format(sys.argv[1]))

# Get random bytes from /dev/random
if sys.argv[1] == "12":
    # Retrieve 128 bit (16 bytes) for 12 words
    entropy = os.getrandom(size=16)
elif sys.argv[1] == "24":
    # Retrieve 256 bit (32 bytes) for 24 words
    entropy = os.getrandom(size=32)

# Convert bytes to binary
binary = ""
for byte in entropy:
    # print(str(bin(byte))[2:].rjust(8, "0"))
    binary += str(bin(byte))[2:].rjust(8, "0")

# Get checksum from entropy
sha256_hash = hashlib.sha256()
sha256_hash.update(entropy)
if sys.argv[1] == "12":
    checksum = str(bin(sha256_hash.digest()[0]))[2:].rjust(8, "0")[:4]
elif sys.argv[1] == "24":
    checksum = str(bin(sha256_hash.digest()[0]))[2:].rjust(8, "0")[:8]

# Combine and print entropy + checksum
binary += checksum
print("Entropy + checksum: {}".format(binary))

# Split entropy into chunks of 11 bit
# Credit: https://stackoverflow.com/a/48707091
size = 11
chunks = [binary[y-size:y] for y in range(size, len(binary)+size,size)]
# print(chunks)

# Get and print word index
print("Word index: ", end="")
words = []
for chunk in chunks:
    words.append(int(chunk, 2))
    print(int(chunk, 2), end=" ")
print("\n")

# Verify wordlist
if hashlib.md5(open("english.txt","rb").read()).hexdigest() != "f23506956964fa69c98fa3fb5c8823b5":
    print("ERROR: english.txt has been modified. Please download the original from https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt.")
    exit()

# Get words from wordlist
with open("english.txt", "r") as wordlist:
    wordlist = wordlist.readlines()
    print("Seed phrase: \33[1;34m", end="")
    for word in words:
        print(wordlist[word][:-1], end=" ")
    print("\33[1;0m\n")

print("\33[1;37mINFO\33[1;0m: It's almost impossible to generate the same seed phrase. Please back up the seed phrase on a piece of paper.")
