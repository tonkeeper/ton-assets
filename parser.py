import json
import os
import shutil

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from to_review.models import AssetData
from to_review.readers import get_blacklist_addresses, get_skip_addresses, get_known_assets_addresses
from utlis import normalize_address
from to_review.presenter import generate_to_review_html, add_blacklist

TON_VIEWER_URL = "https://tonviewer.com/"
TON_API_ACCOUNT_URL = "https://tonapi.io/v2/accounts/"

TO_REVIEW_DIR = "to_review/"
TON_LABELS_DIR = "ton-labels/"
ASSETS_DIR = "assets/"
RETURN_DIR = "../"

BLACKLIST_NFT_TYPES = ["nft_collection", "nft_item", "nft_item_simple"]
BLACKLIST_JETTONS_TYPES = ["jetton_master", "jetton_wallet", "jetton_wallet_governed"]

def clone_ton_labels_repo():
    os.system("git clone https://github.com/ton-studio/ton-labels.git")

def rm_ton_labels_dir():
    shutil.rmtree(TON_LABELS_DIR)

def get_types_from_tonapi(address: str) -> list[str]:
    url = TON_API_ACCOUNT_URL + address
    session = requests.Session()
    retry_strategy = Retry(
        backoff_factor=0.5,
        status_forcelist=[429, 502]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('https://', adapter)
    response = session.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    if not "interfaces" in data:
        return []

    return data["interfaces"]

def is_asset_to_blacklist(types: list[str]):
    # add asset to blacklist if len(types) == 1 and this type is one of jetton types or if it has nft in type
    if len(types) == 1 and types[0] in BLACKLIST_JETTONS_TYPES:
        return True

    for curr_type in types:
        if curr_type in BLACKLIST_NFT_TYPES:
            return True

    return False

# Returns dict of blacklist assets and whitelist assets
def get_asset_from_json_file(file: str, skip_addr_set: set[str]) -> dict[str, list[AssetData]]:
    assets = {"blacklist": [], "whitelist": []}
    with open(file, 'r') as f:
        data = json.load(f)

        label = data['metadata']['label']
        category = data['metadata']['category']
        website = data['metadata']['website']
        description = data['metadata']['description']
        for addr in data['addresses']:
            address = normalize_address(addr['address'], to_raw=False)
            if address in skip_addr_set:
                continue

            link = TON_VIEWER_URL + address
            types = get_types_from_tonapi(address)
            if is_asset_to_blacklist(types):
                assets["blacklist"].append(AssetData(address, link, label, category, website, description))
            else:
                assets["whitelist"].append(AssetData(address, link, label, category, website, description))

    return assets

def get_assets_from_dir(curr_dir: str, skip_addr_set: set[str]) -> dict[str, list[AssetData]]:
    os.chdir(curr_dir)

    assets_from_dir = {"blacklist": [], "whitelist": []}
    for file in os.listdir():
        if not file.endswith(".json"):
            continue # skip not *.json files

        assets_from_file = get_asset_from_json_file(file, skip_addr_set)
        assets_from_dir["blacklist"].extend(assets_from_file["blacklist"])
        assets_from_dir["whitelist"].extend(assets_from_file["whitelist"])

    os.chdir(RETURN_DIR)

    return assets_from_dir

def get_assets_from_dirs(skip_addr_set: set[str]) -> dict[str, list[AssetData]]:
    os.chdir(TON_LABELS_DIR + ASSETS_DIR)

    all_assets = {"blacklist": [], "whitelist": []}
    for curr_dir in os.listdir():
        if os.path.isfile(curr_dir): # skip files
            continue

        assets_from_dir = get_assets_from_dir(curr_dir, skip_addr_set)
        all_assets["blacklist"].extend(assets_from_dir["blacklist"])
        all_assets["whitelist"].extend(assets_from_dir["whitelist"])

    os.chdir(RETURN_DIR + RETURN_DIR)

    return all_assets

def main():
    try:
        os.chdir(TO_REVIEW_DIR)
        clone_ton_labels_repo()

        os.chdir(RETURN_DIR)
        known_addresses = get_known_assets_addresses()
        os.chdir(TO_REVIEW_DIR)

        blacklist_addresses = get_blacklist_addresses()
        skip_addresses = get_skip_addresses()

        known_addresses = known_addresses.union(blacklist_addresses)
        known_addresses = known_addresses.union(skip_addresses)
        assets = get_assets_from_dirs(known_addresses)

        generate_to_review_html(assets["whitelist"])
        add_blacklist(assets["blacklist"])
    finally:
        rm_ton_labels_dir()

if __name__ == "__main__":
    main()