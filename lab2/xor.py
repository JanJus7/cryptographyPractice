# Jan Juszczyński

import argparse
import os

def prepareText():
    inputFile = "orig.txt"
    outputFile = "plain.txt"

    if not os.path.exists(inputFile):
        print(f"BFile missing: {inputFile}")
        return

    with open(inputFile, "r", encoding="ASCII") as infile:
        allText = ""
        for line in infile:
            line = line.strip()
            line = "".join(char for char in line if char.isalpha() or char.isspace())
            line = line.lower()
            allText += line[:35] + "\n"

    with open(outputFile, "w", encoding="ASCII") as outfile:
        outfile.write(allText)

def encryptMessage():
    plainFile = "plain.txt"
    keyFile = "key.txt"
    cryptoFile = "crypto.txt"

    if not os.path.exists(plainFile) or not os.path.exists(keyFile):
        print("File missing (plain.txt or key.txt)")
        return
    
    with open(keyFile, "r", encoding="ASCII") as kfile:
        key = kfile.readline().strip().replace(' ', 'r')
        keyBytes = bytearray(key, encoding="ASCII")
        for i in range(len(keyBytes)):
            keyBytes[i] -= 97

    with open(plainFile, "r", encoding="ASCII") as pfile, open(cryptoFile, "w", encoding="ASCII") as cfile:
        allText = pfile.read().strip()
        textBytes = bytearray(allText, encoding="ASCII")
        x = 0
        out = bytearray()
        for byte in textBytes:
            if x >= len(keyBytes):
                x = 0
            result = byte + keyBytes[x]
            x += 1
            if result > 122:
                result -= 25
            if byte == 10:
                result = 10
                x = 0
            out.append(result)
        cfile.write(out.decode("ASCII"))

def cryptanalysis():
    cryptoFile = "crypto.txt"
    decryptFile = "decrypt.txt"

    if not os.path.exists(cryptoFile):
        print("File missing: crypto.txt")
        return

    with open(cryptoFile, "r", encoding="ASCII") as cfile, open(decryptFile, "w", encoding="ASCII") as dfile:
        lines = cfile.readlines()
        lineLength = len(lines[0].strip())
        arr = []
        for line in lines:
            arr.append(bytearray(line.strip(), encoding="ASCII"))
        
        bytesArr = bytearray(lineLength)
        keyBytes = bytearray(lineLength)
        
        for x in range(len(lines)):
            for y in range(lineLength):
                if arr[x][y] < 58:
                    bytesArr[y] = 32
                    keyBytes[y] = arr[x][y] - bytesArr[y]

        out = ""
        for x in range(len(lines)):
            line = bytearray(lineLength)
            for y in range(lineLength):
                arr[x][y] -= keyBytes[y]
                if 33 < arr[x][y] < 97:
                    arr[x][y] += 25
                line[y] = arr[x][y]
            out += line.decode("ASCII") + "\n"
        dfile.write(out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XOR options: -p, -e, -k")
    parser.add_argument("-p", action="store_true", help="Text preparation")
    parser.add_argument("-e", action="store_true", help="Cypering")
    parser.add_argument("-k", action="store_true", help="Cryptanalysis")

    args = parser.parse_args()

    if args.p:
        prepareText()
    elif args.e:
        encryptMessage()
    elif args.k:
        cryptanalysis()
    else:
        parser.print_help()
