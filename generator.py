#!/bin/env python3
import json

import yaml
import glob
import base64

from dexes import __get_stonfi_assets, __get_megaton_assets, __get_dedust_assets

EXPLORER_JETTONS = "https://tonviewer.com/"
EXPLORER_ACCOUNTS = "https://tonviewer.com/"
EXPLORER_COLLECTIONS = "https://tonviewer.com/"

DEXES_FILE_NAME = "imported_from_dex.yaml"


def collect_all_dexes():
    temp, jettons = list(), list()
    for file in sorted(glob.glob("jettons/*.yaml")):
        if file.endswith(DEXES_FILE_NAME):
            continue
        temp.append(yaml.safe_load(open(file)))

    for item in temp:
        if isinstance(item, list):
            jettons.extend(item)
        else:
            jettons.append(item)

    already_exist_address = dict()
    for jetton in jettons:
        already_exist_address[normalize_address(jetton["address"], True)] = True

    assets = __get_dedust_assets() + __get_stonfi_assets() + __get_megaton_assets()
    assets_for_save = dict()
    for idx, asset in enumerate(assets):
        asset.address = normalize_address(asset.address, True)
        if already_exist_address.get(asset.address, None):
            continue
        assets_for_save[asset.address] = {
            'name': asset.name,
            'address': asset.address,
            'symbol': asset.symbol
        }

    with open(f"jettons/{DEXES_FILE_NAME}", "w") as yaml_file:
        yaml.dump(list(sorted(assets_for_save.values(), key=lambda x: x['symbol'])), yaml_file, default_flow_style=False)

ALLOWED_KEYS =  {'symbol', 'name', 'address', 'description', 'image', 'social', 'websites', 'decimals', 'coinmarketcap', 'coingecko'}

def merge_jettons():
    temp = [yaml.safe_load(open(file)) for file in sorted(glob.glob("jettons/*.yaml"))]
    jettons = []
    for j in temp:
        if isinstance(j, list):
            jettons.extend(j)
        else:
            jettons.append(j)

    already_exist_address = dict()
    for j in jettons:
        if len(set(j.keys()) - ALLOWED_KEYS) > 0:
            raise Exception(f"invalid keys {set(j.keys()) - ALLOWED_KEYS} in {j.get('name')}")
        if len(set(j.keys()) & {"name", "symbol", "address"}) < 3:
            raise Exception(f"name, symbol, and address are required in {j.get('name')}")
        if 'image' in j and j['image'].startswith('https://cache.tonapi.io'):
            raise Exception(f"don't use cache.tonapi.io as image source in {j.get('name')}")

        normalized = normalize_address(j["address"], True)
        if normalized in already_exist_address:
            raise Exception(f"duplicate address for {j['name']} and {already_exist_address[normalized]}")
        already_exist_address[normalized] = j["name"]

        j["address"] = normalized

        for field in ['symbol', 'name', 'address', 'description', 'image', 'coinmarketcap', 'coingecko']:
            if not isinstance(j.get(field, ''), str):
                raise Exception(f"invalid field type for {field} in {j.get('name')}")

        for field in ['social', 'websites']:
            if field in j and (not isinstance(j[field], list) or any(not isinstance(x, str) for x in j[field])):
                raise Exception(f"invalid list field type for {field} in {j.get('name')}")

        if 'decimals' in j:
            j['decimals'] = int(j['decimals'])

    with open('jettons.json', 'w') as out:
        json.dump(jettons, out, indent=" ", sort_keys=True)

    return sorted([(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in jettons])


def merge_accounts(accounts):
    main_page = list()
    for file in ('accounts/infrastructure.yaml', 'accounts/defi.yaml', 'accounts/celebrities.yaml'):
        accs = yaml.safe_load(open(file))
        main_page.extend([(x['name'], x['address']) for x in accs])
        accounts.extend(yaml.safe_load(open(file)))

    files = ('accounts/givers.yaml', 'accounts/custodians.yaml', 'accounts/bridges.yaml', 'accounts/validators.yaml',
             'accounts/scammers.yaml', 'accounts/notcoin.yaml', 'accounts/dapps.yaml')
    for file in files:
        accounts.extend(yaml.safe_load(open(file)))

    for account in accounts:
        account['address'] = normalize_address(account['address'], True)

    with open('accounts.json', 'w') as out:
        json.dump(accounts, out, indent=" ", sort_keys=True)
    return main_page


def merge_collections():
    raw = [yaml.safe_load(open(file)) for file in sorted(glob.glob("collections/*.yaml"))]
    collections = list()

    for c in raw:
        if isinstance(c, list):
            collections.extend(c)
        else:
            collections.append(c)

    for collection in collections:
        collection['address'] = normalize_address(collection['address'], True)

    with open('collections.json', 'w') as out:
        json.dump(collections, out, indent=" ", sort_keys=True)

    return sorted([(c.get('name', 'unknown'), c.get('address', 'unknown')) for c in collections])


def main():
    if len([x for x in glob.glob("*.yaml")]) > 0:
        raise Exception("please don't add yaml files to root directory. use jettons/ or collections/")
    collect_all_dexes()
    jettons = merge_jettons()
    collections = merge_collections()
    # accounts = merge_accounts([{'name': x[0] + " master", 'address': x[1]} for x in jettons])
    accounts = merge_accounts([])
    jettons_md = "\n".join(["[%s](%s%s) | %s" % (j[0], EXPLORER_JETTONS, normalize_address(j[1], True), normalize_address(j[1], False)) for j in jettons])
    accounts_md = "\n".join(["[%s](%s%s) | %s" % (j[0], EXPLORER_ACCOUNTS, normalize_address(j[1], True), normalize_address(j[1], False)) for j in accounts])
    collections_md = "\n".join(["[%s](%s%s) | %s" % (j[0], EXPLORER_COLLECTIONS,  normalize_address(j[1], True), normalize_address(j[1], False)) for j in collections])

    open('README.md', 'w').write(open("readme.md.template").read() % (accounts_md, collections_md))


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


if __name__ == '__main__':
    main()
