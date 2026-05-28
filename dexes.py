import logging
import yaml
from typing import List
import requests

class Asset:
    def __init__(self, name: str, address: str, symbol: str):
        self.name = name
        self.address = address
        self.symbol = symbol


def __get_stonfi_assets() -> List[Asset]:
    url = "https://api.ston.fi/v1/assets"
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("failed to get stonfi assets")
        return list()
    data = response.json()
    assets = list()
    for item in data.get("asset_list", []):
        community = item.get("community", False)
        blacklisted = item.get("blacklisted", False)
        deprecated = item.get("deprecated", False)
        kind = item.get("kind", "")
        if community or blacklisted or deprecated or kind != "Jetton":
            continue
        assets.append(Asset(
            name=item.get("display_name", ""),
            address=item.get("contract_address", ""),
            symbol=item.get("symbol", "")
        ))
    return assets


def __get_megaton_assets() -> List[Asset]:
    url = "https://megaton.fi/api/token/infoList"
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("failed to get megaton assets")
        return list()
    data = response.json()
    assets = list()
    for item in data:
        if item.get("isVisible") != 1 or item.get("type") != 2:
            continue
        assets.append(Asset(
            name=item.get("name", ""),
            address=item.get("address", ""),
            symbol=item.get("symbol", "")
        ))
    return assets


def __get_dedust_assets() -> List[Asset]:
    url = "https://assets.dedust.io/list.json"
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("failed to get dedust assets")
        return list()
    data = response.json()
    assets = list()
    b_addrs = {"EQBiyZMUXvdnRYFUk3_R5uPdsR2ROI9mes_1S-jL1tIQDhDK"}
    for item in data:
        addr = item.get("address")
        if not addr or addr in b_addrs:
            continue
        assets.append(Asset(
            name=item.get("name", ""),
            address=item.get("address", ""),
            symbol=item.get("symbol", "")
        ))
    return assets


def __get_backed_assets() -> List[Asset]:
    url = "https://api.backed.fi/api/v1/token"
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("failed to get backed assets")
        return list()
    data = response.json()
    assets = list()
    for item in data.get('nodes', []):
        ton_addr = ""
        for d in item.get("deployments", []):
            if d.get("network", "").lower() == "ton":
                ton_addr = d.get("address", "").removeprefix("ton:")
        if ton_addr == "":
            continue
        assets.append(Asset(
            name=item.get("name", ""),
            address=ton_addr,
            symbol=item.get("symbol", "")
        ))

    return assets


def update_stonfi_routers():
    response = requests.get("https://api.ston.fi/v1/routers")
    if response.status_code != 200:
        logging.error("failed to update stonfi routers")
        return
    data = response.json()
    routers = list()
    for item in data.get('router_list', []):
        routers.append({"address": item.get("address"), "name": "STON.fi DEX"})
    if len(routers) == 0:
        return
    routers.sort(key=lambda x: x['address'])
    with open("accounts/ston.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(routers, f, sort_keys=True, allow_unicode=True)
