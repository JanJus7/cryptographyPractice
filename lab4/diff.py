#!/usr/bin/env python3

def hexToBin(hexStr):
    return bin(int(hexStr, 16))[2:].zfill(len(hexStr) * 4)

def countDiffBits(hash1, hash2):
    bin1 = hexToBin(hash1)
    bin2 = hexToBin(hash2)
    return sum(bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))

algorithms = [
    "md5sum", "sha1sum", "sha224sum", "sha256sum",
    "sha384sum", "sha512sum", "b2sum"
]

with open("hash.txt", "r") as file:
    hashLines = [line.strip().split()[0] for line in file if line.strip()]

# Zakładamy: 7 hashy dla personal.txt, potem 7+7 = 14 hashy dla połączonych plików
baseIndex = 7
hashPairs = []

for i in range(7):
    hash1 = hashLines[baseIndex + i]
    hash2 = hashLines[baseIndex + 7 + i]
    hashPairs.append((algorithms[i], hash1, hash2))

with open("diff.txt", "w") as outputFile:
    for algorithm, hash1, hash2 in hashPairs:
        totalBits = len(hash1) * 4
        differentBits = countDiffBits(hash1, hash2)
        percentage = differentBits / totalBits * 100
        outputFile.write(f"cat hash-.pdf personal.txt | {algorithm}\n")
        outputFile.write(f"cat hash-.pdf personal_.txt | {algorithm}\n")
        outputFile.write(f"{hash1}\n")
        outputFile.write(f"{hash2}\n")
        outputFile.write(f"Liczba różniących się bitów: {differentBits} z {totalBits}, procentowo: {round(percentage)}%.\n\n")
