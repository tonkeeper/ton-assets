Saeed Fo2hi, [09/25/2025 12:12 ق.ظ]
import glob
import yaml
import json
import base64

EXPLORER_JETTONS = "https://ton.live/jettons/"
EXPLORER_COLLECTIONS = "https://ton.live/collections/"
EXPLORER_ACCOUNTS = "https://ton.live/accounts/"

def collect_all_dexes():
    # Placeholder for your DEX collection logic
    pass

def merge_jettons():
    raw = [yaml.safe_load(open(file)) for file in sorted(glob.glob("jettons/*.yaml"))]
    jettons = []
    for j in raw:
        if isinstance(j, list):
            jettons.extend(j)
        else:
            jettons.append(j)
    return sorted([(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in jettons])

def merge_accounts(accounts):
    # Adjust or fill accounts if needed
    with open('accounts.json', 'w') as out:
        json.dump(accounts, out, indent=" ", sort_keys=True)
    return accounts

def merge_collections():
    raw = [yaml.safe_load(open(file)) for file in sorted(glob.glob("collections/*.yaml"))]
    collections = []
    for c in raw:
        if isinstance(c, list):
            collections.extend(c)
        else:
            collections.append(c)
    with open('collections.json', 'w') as out:
        json.dump(collections, out, indent=" ", sort_keys=True)
    return sorted([(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in collections])

def normalize_address(a, to_raw):
    if len(a) == 48:
        raw = base64.urlsafe_b64decode(a)
        workchain = raw[1]
        if workchain == 255:
            workchain = -1
        addr = raw[2:34]
    elif ":" in a:
        parts = a.split(":")
        if len

Saeed Fo2hi, [09/25/2025 12:20 ق.ظ]
import glob
import yaml
import json
import base64

EXPLORER_JETTONS = "https://ton.live/jettons/"
EXPLORER_COLLECTIONS = "https://ton.live/collections/"
EXPLORER_ACCOUNTS = "https://ton.live/accounts/"

def collect_all_dexes():
    # Placeholder for DEX collection logic if needed
    pass

def merge_jettons():
    raw = [yaml.safe_load(open(file)) for file in sorted(glob.glob("jettons/*.yaml"))]
    jettons = []
    for j in raw:
        if isinstance(j, list):
            jettons.extend(j)
        else:
            jettons.append(j)
    return sorted([(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in jettons])

def merge_accounts(accounts):
    # Adjust or fill accounts if needed
    with open('accounts.json', 'w') as out:
        json.dump(accounts, out, indent=" ", sort_keys=True)
    return accounts

def merge_collections():
    raw = [yaml.safe_load(open(file)) for file in sorted(glob.glob("collections/*.yaml"))]
    collections = []
    for c in raw:
        if isinstance(c, list):
            collections.extend(c)
        else:
            collections.append(c)
    with open('collections.json', 'w') as out:
        json.dump(collections, out, indent=" ", sort_keys=True)
    return sorted([(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in collections])

def normalize_address(a, to_raw):
    if len(a) == 48:
        raw = base64.urlsafe_b64decode(a)
        workchain = raw[1]
        if workchain == 255:
            workchain = -1
        addr = raw[2:34]
    elif ":" in a:
        parts = a.split(":")
        if len(parts) != 2:
            raise Exception("invalid address %s" % a)
        workchain = int(parts[0])
        addr = bytearray.fromhex(parts[1])
    else:
        raise Exception("invalid address %s" % a)
    if to_raw:
        return "%d:%s" % (workchain, addr.hex())

    if workchain == -1:
        workchain = 255
    human = bytearray(36)
    human[0] = 0x11
    human[1] = workchain
    human[2:34] = addr
    human[34:] = crc16(human[:34])
    return base64.urlsafe_b64encode(human).decode()

def crc16(data):
    POLY = 0x1021
    reg = 0
    message = bytes(data) + bytes(2)
    for byte in message:
        mask = 0x80
        while mask > 0:
            reg <<= 1
            if byte & mask:
                reg += 1
            mask >>= 1
            if reg > 0xffff:
                reg &= 0xffff
                reg ^= POLY
    return reg // 256, reg % 256

def main():
    collect_all_dexes()
    jettons = merge_jettons()
    collections = merge_collections()
    accounts = merge_accounts([])

    jettons_md = "\n".join([
        "[%s](%s%s) | %s" % (j[0], EXPLORER_JETTONS, normalize_address(j[1], True), normalize_address(j[1], False))
        for j in jettons
    ])
    accounts_md = "\n".join([
        "[%s](%s%s) | %s" % (j[0], EXPLORER_ACCOUNTS, normalize_address(j[1], True), normalize_address(j[1], False))
        for j in accounts
    ])
    collections_md = "\n".join([
        "[%s](%s%s) | %s" % (j[0], EXPLORER_COLLECTIONS, normalize_address(j[1], True), normalize_address(j[1], False))
        for j in collections
    ])

    template = open("readme.md.template").read()
    open('README.md', 'w').write(template % (accounts_md, collections_md, jettons_md))

if name == 'main':
    main()
