def hexToBin(hexString):
    return bin(int(hexString, 16))[2:].zfill(len(hexString) * 4)

def countDifferentBits(hash1, hash2):
    bin1 = hexToBin(hash1)
    bin2 = hexToBin(hash2)
    differentBits = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
    totalBits = len(bin1)
    percentage = (differentBits / totalBits) * 100
    return differentBits, totalBits, percentage

def generateDiffFile():
    algorithms = [
        "md5sum", "sha1sum", "sha224sum", "sha256sum",
        "sha384sum", "sha512sum", "b2sum"
    ]

    with open("hash.txt", "r") as file:
        hashLines = [line.strip().split()[0] for line in file if line.strip()]

    baseIndex = 7
    hashPairs = []

    for i in range(7):
        hash1 = hashLines[baseIndex + i]
        hash2 = hashLines[baseIndex + 7 + i]
        hashPairs.append((algorithms[i], hash1, hash2))

    with open("diff.txt", "w") as outputFile:
        for algorithm, hash1, hash2 in hashPairs:
            differentBits, totalBits, percentage = countDifferentBits(hash1, hash2)
            outputFile.write(f"cat hash-.pdf personal.txt | {algorithm}\n")
            outputFile.write(f"cat hash-.pdf personal_.txt | {algorithm}\n")
            outputFile.write(f"{hash1}\n")
            outputFile.write(f"{hash2}\n")
            outputFile.write(
                f"Liczba różniących się bitów: {differentBits} z {totalBits}, procentowo: {percentage:.0f}%.\n\n"
            )

generateDiffFile()
