# Jan Juszczyński

import argparse
import secrets
import math
import sys

def readTwoNumbers(filename):
    with open(filename, 'r') as f:
        tokens = f.read().split()
    if len(tokens) < 2:
        sys.exit(f"Error: {filename} needs to contain two numbers...")
    p = int(tokens[0])
    g = int(tokens[1])
    return p, g

def keyGen():
    p, g = readTwoNumbers('elgamal.txt')
    x = secrets.randbelow(p-2) + 1
    y = pow(g, x, p)
    with open('private.txt', 'w') as f:
        f.write(f"{p}\n{g}\n{x}\n")
    with open('public.txt', 'w') as f:
        f.write(f"{p}\n{g}\n{y}\n")

def encrypt():
    p, g = readTwoNumbers('public.txt')
    _, _, y = map(int, open('public.txt', 'r').read().split())
    try:
        m = int(open('plain.txt', 'r').read().strip())
    except:
        sys.exit("Error: unable to read number from plain.txt")
    if m >= p:
        print("Error: message needs to be < p", file=sys.stderr)
        sys.exit(1)
    k = secrets.randbelow(p-2) + 1
    a = pow(g, k, p)
    b = (m * pow(y, k, p)) % p
    with open('crypto.txt', 'w') as f:
        f.write(f"{a}\n{b}\n")

def decrypt():
    p, g = readTwoNumbers('private.txt')
    _, _, x = map(int, open('private.txt', 'r').read().split())
    try:
        a, b = map(int, open('crypto.txt', 'r').read().split())
    except:
        sys.exit("Error: unable to read pair from crypto.txt")
    m = (b * pow(a, p-1-x, p)) % p
    with open('decrypt.txt', 'w') as f:
        f.write(f"{m}\n")

def sign():
    p, g = readTwoNumbers('private.txt')
    _, _, x = map(int, open('private.txt', 'r').read().split())
    try:
        m = int(open('message.txt', 'r').read().strip())
    except:
        sys.exit("Error: unable to read a num from message.txt")
    while True:
        k = secrets.randbelow(p-2) + 1
        if math.gcd(k, p-1) == 1:
            break
    r = pow(g, k, p)
    kInv = pow(k, -1, p-1)
    s = ((m - x * r) * kInv) % (p-1)
    with open('signature.txt', 'w') as f:
        f.write(f"{r}\n{s}\n")

def verify():
    p, g = readTwoNumbers('public.txt')
    _, _, y = map(int, open('public.txt', 'r').read().split())
    try:
        m = int(open('message.txt', 'r').read().strip())
    except:
        sys.exit("Error: unable to read a num from message.txt")
    try:
        r, s = map(int, open('signature.txt', 'r').read().split())
    except:
        sys.exit("Error: unable to read pair from signature.txt")
    left = (pow(y, r, p) * pow(r, s, p)) % p
    right = pow(g, m, p)
    result = 'T' if left == right else 'N'
    print(result)
    with open('verify.txt', 'w') as f:
        f.write(f"{result}\n")

parser = argparse.ArgumentParser(description="ElGamal")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-k', action='store_true', help='gen keys')
group.add_argument('-e', action='store_true', help='encrypt')
group.add_argument('-d', action='store_true', help='decrypt')
group.add_argument('-s', action='store_true', help='sign')
group.add_argument('-v', action='store_true', help='verify')

args = parser.parse_args()

if args.k:
    keyGen()
elif args.e:
    encrypt()
elif args.d:
    decrypt()
elif args.s:
    sign()
elif args.v:
    verify()
