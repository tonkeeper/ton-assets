#!/bin/env python3
import json
import glob
import base64
import yaml

from dexes import __get_stonfi_assets, __get_megaton_assets, __get_dedust_assets

EXPLORER_JETTONS = "https://tonviewer.com/"
EXPLORER_ACCOUNTS = "https://tonviewer.com/"
EXPLORER_COLLECTIONS = "https://tonviewer.com/"

DEXES_FILE_NAME = "imported_from_dex.yaml"

ALLOWED_KEYS = {
    'symbol', 'name', 'address', 'description', 'image', 'social', 'websites',
    'decimals', 'coinmarketcap', 'coingecko', 'token', 'issuer', 'technical', 'ticker'
}


def collect_all_dexes():
    temp, jettons = list(), list()
    for file in sorted(glob.glob("jettons/*.yaml")):
        if file.endswith(DEXES_FILE_NAME):
            continue
        try:
            with open(file, encoding='utf-8') as f:
                content = yaml.safe_load(f)
                if content:
                    if isinstance(content, list):
                        temp.extend(content)
                    else:
                        temp.append(content)
                else:
                    print(f"Warning: {file} is empty or invalid.")
        except yaml.YAMLError as e:
            print(f"Error parsing {file}: {e}")

    already_exist_address = dict()
    for jetton in temp:
        if isinstance(jetton, dict) and "technical" in jetton and "contract_address" in jetton["technical"]:
            jetton["address"] = jetton["technical"]["contract_address"]

        if "address" not in jetton or not jetton["address"]:
            print(f"Error: Missing 'address' in jetton: {jetton}")
            continue

        try:
            normalized_address = normalize_address(jetton["address"], True)
        except Exception as e:
            print(f"Error normalizing address for jetton {jetton.get('name', 'unknown')}: {e}")
            continue

        already_exist_address[normalized_address] = True

    assets = __get_dedust_assets() + __get_stonfi_assets() + __get_megaton_assets()
    assets_for_save = dict()
    for asset in assets:
        normalized_address = normalize_address(asset.address, True)
        if normalized_address not in already_exist_address:
            assets_for_save[normalized_address] = {
                'name': asset.name,
                'address': asset.address,
                'symbol': asset.symbol
            }

    with open(f"jettons/{DEXES_FILE_NAME}", "w") as yaml_file:
        yaml.dump(list(assets_for_save.values()), yaml_file, default_flow_style=False)


def merge_jettons():
    temp = []
    for file in sorted(glob.glob("jettons/*.yaml")):
        try:
            with open(file, encoding='utf-8') as f:
                content = yaml.safe_load(f)
                if content:
                    temp.append(content)
                else:
                    print(f"Warning: File {file} is empty or invalid and will be skipped.")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file {file}: {e}")
            continue

    jettons = []
    for j in temp:
        if isinstance(j, list):
            jettons.extend(j)
        else:
            jettons.append(j)

    already_exist_address = dict()
    for j in jettons:
        if 'token' in j:
            j['name'] = j['token'].get('name')
            j['symbol'] = j.get('ticker')
        if 'technical' in j:
            j['address'] = j['technical'].get('contract_address')

        if len(set(j.keys()) & {"name", "symbol", "address"}) < 3:
            print(f"Warning: Skipping jetton with missing required fields: {j}")
            continue
        if set(j.keys()) - ALLOWED_KEYS:
            print(f"Warning: Jetton {j.get('name', 'unknown')} contains invalid keys: {set(j.keys()) - ALLOWED_KEYS}")
            continue

        try:
            normalized = normalize_address(j["address"], True)
        except Exception as e:
            print(f"Warning: Skipping jetton due to invalid address: {j.get('name', 'unknown')} - {e}")
            continue

        if normalized in already_exist_address:
            print(f"Warning: Duplicate address found for {j['name']} and {already_exist_address[normalized]}")
            continue
        already_exist_address[normalized] = j["name"]

    with open('jettons.json', 'w') as out:
        json.dump(jettons, out, indent=4, sort_keys=True)
    return sorted([(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in jettons])


def merge_accounts(accounts):
    main_page = list()
    for file in ('accounts/infrastructure.yaml', 'accounts/defi.yaml', 'accounts/celebrities.yaml'):
        with open(file, encoding='utf-8') as f:
            accs = yaml.safe_load(f)
            main_page.extend([(x['name'], x['address']) for x in accs])
            accounts.extend(accs)
    for file in ('accounts/givers.yaml', 'accounts/custodians.yaml', 'accounts/bridges.yaml',
                 'accounts/validators.yaml', 'accounts/scammers.yaml', 'accounts/notcoin.yaml'):
        with open(file, encoding='utf-8') as f:
            accounts.extend(yaml.safe_load(f))

    with open('accounts.json', 'w') as out:
        for a in accounts:
            a['address'] = normalize_address(a['address'], True)
        json.dump(accounts, out, indent=" ", sort_keys=True)
    return main_page


def merge_collections():
    raw = [yaml.safe_load(open(file, encoding='utf-8')) for file in sorted(glob.glob("collections/*.yaml"))]
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
    if not a:
        raise Exception("Missing address")
    if len(a) == 48:
        try:
            if not to_raw:
                return a
            raw = base64.urlsafe_b64decode(a)
            workchain = raw[1]
            if workchain == 255:
                workchain = -1
            addr = raw[2:34]
            return f"{workchain}:{addr.hex()}"
        except Exception:
            raise Exception(f"Invalid Base64 address format: {a}")

    elif ":" in a:
        parts = a.split(":")
        if len(parts) != 2:
            raise Exception(f"Invalid address format: {a}")
        workchain = int(parts[0])
        addr = bytearray.fromhex(parts[1])
        if to_raw:
            return f"{workchain}:{addr.hex()}"
        else:
            human = bytearray(36)
            human[0] = 0x11
            human[1] = 255 if workchain == -1 else workchain
            human[2:34] = addr
            human[34:] = crc16(human[:34])
            return base64.urlsafe_b64encode(human).decode()

    else:
        raise Exception(f"Invalid address format: {a}")


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

    with open("readme.md.template", encoding="utf-8") as template_file:
        readme_content = template_file.read() % (accounts_md, collections_md, jettons_md)
    with open('README.md', 'w', encoding="utf-8") as md_file:
        md_file.write(readme_content)


if __name__ == '__main__':
    main()
