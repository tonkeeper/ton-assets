#!/bin/env python3
import json
import yaml
import glob
import base64
import math

EXPLORER_JETTONS = "https://tonapi.io/jetton/"
EXPLORER_ACCOUNTS = "https://tonapi.io/account/"
EXPLORER_COLLECTIONS = "https://tonscan.org/nft/"


def merge_jettons():
    temp = [yaml.safe_load(open(file)) for file in sorted(glob.glob("jettons/*.yaml"))]
    jettons = []
    for j in temp:
        if isinstance(j, list):
            jettons.extend(j)
        else:
            jettons.append(j)
    with open('jettons.json', 'w') as out:
        json.dump(jettons, out, indent=" ", sort_keys=True)
    return sorted([(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in jettons])


def merge_accounts(accounts):
    main_page = list()
    for file in ('accounts/infrastructure.yaml', 'accounts/defi.yaml', 'accounts/celebrities.yaml'):
        accs = yaml.safe_load(open(file))
        main_page.extend([(x['name'], x['address']) for x in accs])
        accounts.extend(yaml.safe_load(open(file)))
    for file in ('accounts/givers.yaml', 'accounts/custodians.yaml', 'accounts/bridges.yaml', 'accounts/validators.yaml'):
        accounts.extend(yaml.safe_load(open(file)))
    with open('accounts.json', 'w') as out:
        for a in accounts:
            a['address'] = normalize_address(a['address'], True)
        json.dump(accounts, out, indent=" ", sort_keys=True)
    return main_page


def merge_collections():
    collections = [yaml.safe_load(open(file)) for file in sorted(glob.glob("collections/*.yaml"))]
    with open('collections.json', 'w') as out:
        json.dump(collections, out, indent=" ", sort_keys=True)
    return sorted([(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in collections])


def main():
    jettons = merge_jettons()
    collections = merge_collections()
    accounts = merge_accounts([{"name": x[0], "address": x[1]} for x in jettons+collections])
    jettons_md = "\n".join(["[%s](%s%s) | %s" % (j[0], EXPLORER_JETTONS, normalize_address(j[1], True), normalize_address(j[1], False)) for j in jettons])
    accounts_md = "\n".join(["[%s](%s%s) | %s" % (j[0], EXPLORER_ACCOUNTS, normalize_address(j[1], True), normalize_address(j[1], False)) for j in accounts])
    collections_md = "\n".join(["[%s](%s%s) | %s" % (j[0], EXPLORER_COLLECTIONS,  normalize_address(j[1], True), normalize_address(j[1], False)) for j in collections])

    open('README.md', 'w').write(open("readme.md.template").read() % (accounts_md, collections_md, jettons_md))


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


if __name__ == '__main__':
    main()
