# Juszczyński Jan

import argparse
import math


def cezarEncrypt(text, shift):
    result = ""
    for c in text:
        if c.isalpha():
            shiftAmount = shift % 26
            if c.islower():
                result += chr(((ord(c) - 97 + shiftAmount) % 26) + 97)
            else:
                result += chr(((ord(c) - 65 + shiftAmount) % 26) + 65)
        else:
            result += c
    return result


def cezarDecrypt(text, shift):
    return cezarEncrypt(text, -shift)


def affineEncrypt(text, a, b):
    result = ""
    for c in text:
        if c.isalpha():
            if c.islower():
                result += chr(((a * (ord(c) - 97) + b) % 26) + 97)
            else:
                result += chr(((a * (ord(c) - 65) + b) % 26) + 65)
        else:
            result += c
    return result


def modInverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None


def affineDecrypt(text, a, b):
    if math.gcd(a, 26) != 1:
        raise ValueError(f"Klucz 'a' = {a} nie ma odwrotności modulo 26")

    aInv = modInverse(a, 26)
    result = ""
    for c in text:
        if c.isalpha():
            if c.islower():
                result += chr(((aInv * (ord(c) - 97 - b)) % 26) + 97)
            else:
                result += chr(((aInv * (ord(c) - 65 - b)) % 26) + 65)
        else:
            result += c
    return result


def readFile(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def writeFile(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def affineKnownTextAttack(cryptoText, plainText):
    for a in range(1, 26):
        if math.gcd(a, 26) == 1:
            for b in range(26):
                decrypted = affineDecrypt(cryptoText, a, b)
                if plainText in decrypted:
                    return a, b, decrypted
    return None, None, None


def affineBruteForce(cryptoText):
    results = []
    for a in range(1, 26):
        if math.gcd(a, 26) == 1:
            for b in range(26):
                decrypted = affineDecrypt(cryptoText, a, b)
                results.append((a, b, decrypted))
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Program do szyfrowania i deszyfrowania"
    )
    parser.add_argument("-c", "--cezar", action="store_true", help="Użyj szyfru Cezara")
    parser.add_argument(
        "-a", "--affine", action="store_true", help="Użyj szyfru afinicznego"
    )
    parser.add_argument("-e", "--encrypt", action="store_true", help="Szyfrowanie")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Deszyfrowanie")
    parser.add_argument(
        "-j", "--knowntext", action="store_true", help="Kryptoanaliza z tekstem jawnym"
    )
    parser.add_argument(
        "-k", "--bruteforce", action="store_true", help="Kryptoanaliza brute-force"
    )

    args = parser.parse_args()

    if args.cezar:
        if args.encrypt:
            plainText = readFile("plain.txt")
            keyData = readFile("key.txt").split()
            if keyData:
                key = int(keyData[0])
                result = cezarEncrypt(plainText, key)
                writeFile("crypto.txt", result)
            else:
                print("Błąd: Brak klucza w pliku key.txt")
        elif args.decrypt:
            cryptoText = readFile("crypto.txt")
            keyData = readFile("key.txt").split()
            if keyData:
                key = int(keyData[0])
                result = cezarDecrypt(cryptoText, key)
                writeFile("decrypt.txt", result)
            else:
                print("Błąd: Brak klucza w pliku key.txt")
        elif args.knowntext:
            cryptoText = readFile("crypto.txt")
            extraText = readFile("extra.txt")
            if cryptoText and extraText:
                for shift in range(1, 26):
                    decrypted = cezarDecrypt(cryptoText, shift)
                    if extraText in decrypted:
                        writeFile("key-found.txt", str(shift))
                        writeFile("decrypt.txt", decrypted)
                        break
                else:
                    print("Błąd: Nie znaleziono klucza")
            else:
                print("Błąd: Brak plików crypto.txt lub extra.txt")
        elif args.bruteforce:
            cryptoText = readFile("crypto.txt")
            if cryptoText:
                with open("decrypt.txt", "w", encoding="utf-8") as f:
                    for shift in range(1, 26):
                        decrypted = cezarDecrypt(cryptoText, shift)
                        f.write(f"Przesunięcie {shift}:\n{decrypted}\n\n")
            else:
                print("Błąd: Brak pliku crypto.txt")

    elif args.affine:
        if args.encrypt:
            plainText = readFile("plain.txt")
            keyData = readFile("key.txt").split()
            if len(keyData) == 2:
                a, b = map(int, keyData)
                if math.gcd(a, 26) == 1:
                    result = affineEncrypt(plainText, a, b)
                    writeFile("crypto.txt", result)
                else:
                    print(f"Błąd: Klucz 'a' = {a} nie spełnia warunku NWD(a,26) = 1")
            else:
                print("Błąd: Nieprawidłowy format klucza w pliku key.txt")
        elif args.decrypt:
            cryptoText = readFile("crypto.txt")
            keyData = readFile("key.txt").split()
            if len(keyData) == 2:
                a, b = map(int, keyData)
                if math.gcd(a, 26) == 1:
                    result = affineDecrypt(cryptoText, a, b)
                    writeFile("decrypt.txt", result)
                else:
                    print(f"Błąd: 'a' = {a} nie spełnia NWD(a,26) = 1")
            else:
                print("Błąd: Nieprawidłowy format klucza w pliku key.txt")
        elif args.knowntext:
            cryptoText = readFile("crypto.txt")
            extraText = readFile("extra.txt")
            if cryptoText and extraText:
                a, b, decrypted = affineKnownTextAttack(cryptoText, extraText)
                if a is not None:
                    writeFile("key-found.txt", f"{a} {b}")
                    writeFile("decrypt.txt", decrypted)
                else:
                    print("Błąd: Nie znaleziono klucza")
            else:
                print("Błąd: Brak plików crypto.txt lub extra.txt")
        elif args.bruteforce:
            cryptoText = readFile("crypto.txt")
            if cryptoText:
                results = affineBruteForce(cryptoText)
                with open("decrypt.txt", "w", encoding="utf-8") as f:
                    for a, b, decrypted in results:
                        f.write(f"Klucz a={a}, b={b}:\n{decrypted}\n\n")
            else:
                print("Błąd: Brak pliku crypto.txt")

    else:
        print("Błędne argumenty! Użyj --help, aby zobaczyć opcje.")
