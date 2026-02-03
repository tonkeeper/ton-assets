import logging
import yaml
from typing import List

import requests
from pydantic import BaseModel


class Asset(BaseModel):
    name: str
    address: str
    symbol: str


class MegatonAsset(Asset):
    type: int
    isVisible: int


class StonfiAsset(BaseModel):
    contract_address: str
    display_name: str
    symbol: str
    kind: str
    decimals: int
    community: bool
    deprecated: bool
    blacklisted: bool


def __get_stonfi_assets() -> List[Asset]:
    url = "https://api.ston.fi/v1/assets"
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("failed to get stonfi assets")
        return list()
    data = response.json()
    stonfi_assets = [StonfiAsset(**item) for item in data["asset_list"]]
    assets = list()
    for asset in stonfi_assets:
        if asset.community or asset.blacklisted or asset.deprecated or asset.kind != "Jetton":
            continue
        assets.append(Asset(name=asset.display_name, address=asset.contract_address, symbol=asset.symbol))
    return assets


def __get_megaton_assets() -> List[Asset]:
    url = "https://megaton.fi/api/token/infoList"
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("failed to get megaton assets")
        return list()
    data = response.json()
    megaton_assets = [MegatonAsset(**item) for item in data]
    assets = list()
    for asset in megaton_assets:
        if asset.isVisible != 1 or asset.type != 2:
            continue
        assets.append(Asset(name=asset.name, address=asset.address, symbol=asset.symbol))
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
        assets.append(Asset(**item))
    return assets


def __get_backed_assets() -> List[Asset]:
    url = "https://api.backed.fi/api/v1/token"
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("failed to get dedust assets")
        return list()
    data = response.json()
    assets = list()
    for item in data['nodes']:
        ton_addr = ""
        for d in item["deployments"]:
            if d["network"].lower() == "ton":
                ton_addr = d["address"].removeprefix("ton:")
        if ton_addr == "":
            continue
        assets.append(Asset(name=item["name"], address=ton_addr, symbol=item["symbol"]))

    return assets


def update_stonfi_routers():
    response = requests.get("https://api.ston.fi/v1/routers")
    if response.status_code != 200:
        logging.error("failed to update stonfi routers")
        return
    data = response.json()
    routers = list()
    for item in data['router_list']:
        routers.append({"address": item["address"], "name": "STON.fi DEX"})
    if len(routers) == 0:
        return
    with open("accounts/ston.yaml", "w") as f:
        yaml.safe_dump(routers, f, sort_keys=True, allow_unicode=True)
