import logging
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
    url = "https://assets.dedust.io/ton/all.json"
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("failed to get dedust assets")
        return list()
    data = response.json()
    assets = list()
    for item in data:
        if not item.get("address"):
            continue
        assets.append(Asset(**item))
    return assets
