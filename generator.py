#!/bin/env python3
import json
import yaml
import glob

EXPLORER_JETTONS = "https://tonapi.io/jetton/"
EXPLORER_ACCOUNTS = "https://tonapi.io/jetton/"
EXPLORER_COLLECTIONS = "https://tonscan.org/nft/"


def merge_jettons():
    jettons = [yaml.safe_load(open(file)) for file in glob.glob("jettons/*.yaml")]
    with open('jettons.json', 'w') as out:
        json.dump(jettons, out, indent=" ")
    return [(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in jettons]


def merge_accounts(accounts):
    main_page = list()
    for file in ('accounts/infrastructure.yaml', 'accounts/defi.yaml', 'accounts/celebrities.yaml'):
        accs = yaml.safe_load(open(file))
        main_page.extend([(x['name'], x['address']) for x in accs])
        accounts.extend(yaml.safe_load(open(file)))
    for file in ('accounts/givers.yaml', 'accounts/custodians.yaml', 'accounts/bridges.yaml', 'accounts/validators.yaml'):
        accounts.extend(yaml.safe_load(open(file)))
    with open('accounts.json', 'w') as out:
        json.dump(accounts, out, indent=" ")
    return main_page


def merge_collections():
    collections = [yaml.safe_load(open(file)) for file in glob.glob("collections/*.yaml")]
    with open('collections.json', 'w') as out:
        json.dump(collections, out, indent=" ")
    return [(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in collections]


def main():
    jettons = merge_jettons()
    collections = merge_collections()
    accounts = merge_accounts([{"name":x[0], "address": x[1]} for x in jettons+collections])
    jettons_md = "\n".join(["[%s](%s%s) | %s" %(j[0],EXPLORER_JETTONS, j[1], j[1]) for j in jettons])
    accounts_md = "\n".join(["[%s](%s%s) | %s" %(j[0], EXPLORER_ACCOUNTS, j[1], j[1]) for j in accounts])
    collections_md = "\n".join(["[%s](%s%s) | %s" % (j[0], EXPLORER_COLLECTIONS, j[1], j[1]) for j in collections])

    open('README.md', 'w').write(open("readme.md.template").read() % (accounts_md, collections_md, jettons_md) )


if __name__ == '__main__':
    main()
