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
