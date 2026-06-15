import csv
import json
import os

from utlis import normalize_address

def get_known_assets_addresses() -> set[str]:
    addresses = set()

    for file in os.listdir():
        if not file.endswith(".json"): # skip not .json files
            continue

        data_list = json.load(open(file))
        for curr in data_list:
            if "address" not in curr:
                continue # skip if dont contain address

            addresses.add(normalize_address(curr["address"], to_raw=False))

    return addresses

def get_blacklist_addresses() -> set[str]:
    addresses = set()
    with open("blacklist.csv", mode='r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            addresses.add(row[0])

    return addresses

def get_skip_addresses() -> set[str]:
    addresses = set()
    with open("skip_list.csv", mode='r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            addresses.add(row[0])

    return addresses