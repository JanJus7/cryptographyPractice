# Jan Juszczyński
import numpy as np
from PIL import Image, ImageOps
import os

BLOCK_SIZE = 16

def main(filePath: str):
    imageMatrix = readBmpImg(filePath)
    key = getKey().encode('utf-8')
    iv = bytes([0]*BLOCK_SIZE)
    
    imageEcb = encryptImg(imageMatrix.copy(), key, mode="ECB", iv=iv)
    saveImg(imageEcb, "ecb_crypto.bmp")
    
    imageCbc = encryptImg(imageMatrix.copy(), key, mode="CBC", iv=iv)
    saveImg(imageCbc, "cbc_crypto.bmp")


def encryptBlock(block: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(block)])


def encryptImg(image: np.ndarray, key: bytes, mode: str, iv: bytes) -> np.ndarray:
    height, width = image.shape
    flat = image.flatten()
    paddedLength = ((len(flat) + BLOCK_SIZE - 1) // BLOCK_SIZE) * BLOCK_SIZE
    padded = np.pad(flat, (0, paddedLength - len(flat)), 'constant', constant_values=0)
    
    encrypted = bytearray()
    prevBlock = iv

    for i in range(0, len(padded), BLOCK_SIZE):
        block = padded[i:i+BLOCK_SIZE].tobytes()
        
        if mode == "ECB":
            encryptedBlock = encryptBlock(block, key)
        elif mode == "CBC":
            blockXor = bytes([b ^ pb for b, pb in zip(block, prevBlock)])
            encryptedBlock = encryptBlock(blockXor, key)
            prevBlock = encryptedBlock
        else:
            raise ValueError("Unknown cyphering mode...")

        encrypted.extend(encryptedBlock)

    encryptedArr = np.frombuffer(encrypted, dtype=np.uint8)[:len(flat)]
    return encryptedArr.reshape((height, width))


def saveImg(imageArr: np.ndarray, filename: str) -> None:
    image = Image.fromarray(imageArr)
    image.save(filename, format='bmp')


def readBmpImg(filePath):
    try:
        image = Image.open(filePath)
        grayScale = ImageOps.grayscale(image)
        return np.array(grayScale)
    except IOError:
        print("Unable to open image file.")
        exit(1)


def getKey() -> str:
    filename = "key.txt"
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            return file.read().strip()
    else:
        return "Key to destruction xD"


if __name__ == "__main__":
    main("plain.bmp")
