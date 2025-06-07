# Jan Juszczyński

import re
from pathlib import Path
import argparse

def readMessageBits(filePath):
    hexString = Path(filePath).read_text().strip()
    return ''.join(f"{int(h, 16):04b}" for h in hexString)

def writeMessageBits(bits, filePath):
    if len(bits) % 4 != 0:
        bits = bits[:len(bits) // 4 * 4]
    hexString = ''.join(f"{int(bits[i:i+4], 2):x}" for i in range(0, len(bits), 4))
    Path(filePath).write_text(hexString)

def cleanCarrier(content, mode):
    if mode == 1:
        return '\n'.join(line.rstrip() for line in content.splitlines())
    elif mode == 2:
        return re.sub(r' {2,}', ' ', content)
    elif mode == 3:
        return re.sub(r'margin-botom', 'margin-bottom', content, flags=re.IGNORECASE)
    elif mode == 4:
        content = re.sub(r'<FONT></FONT><FONT>', '<FONT>', content, flags=re.IGNORECASE)
        content = re.sub(r'</FONT><FONT>', '</FONT>', content, flags=re.IGNORECASE)
        content = re.sub(r'</FONT><FONT></FONT>', '</FONT>', content, flags=re.IGNORECASE)
        return content
    return content

def embedMode1(carrier, bits):
    lines = carrier.splitlines()
    if len(bits) > len(lines):
        raise ValueError("Za malo linii do zakodowania wiadomosci")
    result = [line + (' ' if i < len(bits) and bits[i] == '1' else '') for i, line in enumerate(lines)]
    return '\n'.join(result)

def extractMode1(content):
    return ''.join(['1' if line.endswith(' ') else '0' for line in content.splitlines()])

def embedMode2(content, bits):
    spaces = [m.start() for m in re.finditer(r'(?<! ) (?! )', content)]
    if len(bits) > len(spaces):
        raise ValueError("Za malo spacji do zakodowania wiadomosci")
    chars = list(content)
    for bit, pos in zip(bits, spaces):
        if bit == '1':
            chars[pos] = '  '
    return ''.join(chars)

def extractMode2(content):
    return ''.join(['1' if m.group(0) == '  ' else '0' for m in re.finditer(r' {1,2}', content)])

def embedMode3(content, bits):
    matches = list(re.finditer(r'<p style="[^"]*">', content, flags=re.IGNORECASE))
    if len(bits) > len(matches):
        raise ValueError("Za malo tagow do zakodowania wiadomosci")
    offset = 0
    for i, bit in enumerate(bits):
        match = matches[i]
        tag = match.group(0)
        newTag = tag
        if bit == '0' and 'margin-bottom' in tag:
            newTag = tag.replace('margin-bottom', 'margin-botom')
        elif bit == '1' and 'line-height' in tag:
            newTag = tag.replace('line-height', 'lineheight')
        start = match.start() + offset
        end = match.end() + offset
        content = content[:start] + newTag + content[end:]
        offset += len(newTag) - len(tag)
    return content

def extractMode3(content):
    bits = []
    for match in re.finditer(r'<p style="[^"]*">', content, flags=re.IGNORECASE):
        tag = match.group(0).lower()
        if 'margin-botom' in tag:
            bits.append('0')
        elif 'lineheight' in tag:
            bits.append('1')
    return ''.join(bits)

def embedMode4(content, bits):
    fontOpenTags = list(re.finditer(r'<font\b[^>]*>', content, flags=re.IGNORECASE))
    fontCloseTags = list(re.finditer(r'</font>', content, flags=re.IGNORECASE))
    if len(bits) > min(len(fontOpenTags), len(fontCloseTags)):
        raise ValueError("Za mało znaczników FONT do zakodowania wiadomości")
    result = []
    lastPos = 0
    openIdx = 0
    closeIdx = 0
    for bit in bits:
        nextOpen = fontOpenTags[openIdx]
        nextClose = fontCloseTags[closeIdx]
        result.append(content[lastPos:nextOpen.start()])
        if bit == '1':
            result.append('<font></font><font>')
        else:
            result.append(content[nextOpen.start():nextOpen.end()])
        lastPos = nextOpen.end()
        openIdx += 1
        result.append(content[lastPos:nextClose.end()])
        if bit == '0':
            result.append('<font></font>')
        lastPos = nextClose.end()
        closeIdx += 1
    result.append(content[lastPos:])
    return ''.join(result)

def extractMode4(content):
    bits = []
    i = 0
    content = content.lower()
    while i < len(content):
        if content.startswith('<font></font><font>', i):
            bits.append('1')
            i += len('<font></font><font>')
        elif content.startswith('</font><font></font>', i):
            bits.append('0')
            i += len('</font><font></font>')
        else:
            i += 1
    return ''.join(bits)

parser = argparse.ArgumentParser()
parser.add_argument('-e', action='store_true', help='embed')
parser.add_argument('-d', action='store_true', help='detect')
parser.add_argument('-1', action='store_true')
parser.add_argument('-2', action='store_true')
parser.add_argument('-3', action='store_true')
parser.add_argument('-4', action='store_true')
args = parser.parse_args()

mode = 1 if args.__dict__['1'] else 2 if args.__dict__['2'] else 3 if args.__dict__['3'] else 4

if args.e:
    bits = readMessageBits('mess.txt')
    content = Path('cover.html').read_text()
    content = cleanCarrier(content, mode)
    if mode == 1:
        out = embedMode1(content, bits)
    elif mode == 2:
        out = embedMode2(content, bits)
    elif mode == 3:
        out = embedMode3(content, bits)
    elif mode == 4:
        out = embedMode4(content, bits)
    Path('watermark.html').write_text(out)

elif args.d:
    content = Path('watermark.html').read_text()
    if mode == 1:
        bits = extractMode1(content)
    elif mode == 2:
        bits = extractMode2(content)
    elif mode == 3:
        bits = extractMode3(content)
    elif mode == 4:
        bits = extractMode4(content)
    originalLength = len(readMessageBits('mess.txt'))
    bits = bits[:originalLength]
    writeMessageBits(bits, 'detect.txt')
