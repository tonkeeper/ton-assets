#!/bin/env python3
import json
import yaml
import glob

EXPLORER_JETTONS = "https://tonapi.io/jetton/"
EXPLORER_ACCOUNTS = "https://tonapi.io/jetton/"

def merge_jettons():
    jettons = [yaml.safe_load(open(file)) for file in glob.glob("jettons/*.yaml")]
    with open('jettons.json', 'w') as out:
        json.dump(jettons, out, indent=" ")
    return [(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in jettons]


def merge_accounts():
    accounts = list()
    main_page = list()
    for file in ('accounts/infrastructure.yaml',):
        accs = yaml.safe_load(open(file))
        main_page.extend([(x['name'], x['address']) for x in accs])
        accounts.extend(yaml.safe_load(open(file)))
    for file in ('accounts/givers.yaml', 'accounts/custodians.yaml'):
        accounts.extend(yaml.safe_load(open(file)))
    with open('accounts.json', 'w') as out:
        json.dump(accounts, out, indent=" ")
    return main_page


def main():
    jettons = merge_jettons()
    accounts = merge_accounts()
    jettons_md = "\n".join(["[%s](%s%s) | %s" %(j[0],EXPLORER_JETTONS, j[1], j[1]) for j in jettons])
    accounts_md = "\n".join(["[%s](%s%s) | %s" %(j[0], EXPLORER_ACCOUNTS, j[1], j[1]) for j in accounts])

    open('README.md', 'w').write(open("readme.md.template").read() % (accounts_md, jettons_md) )


if __name__ == '__main__':
    main()