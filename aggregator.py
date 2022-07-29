#!/bin/env python3
import json
import yaml
import glob

def merge_jettons():
    jettons = [yaml.safe_load(open(file)) for file in glob.glob("jettons/*.yaml")]
    with open('jettons.json', 'w') as out:
        json.dump(jettons, out, indent=" ")
    return [(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in jettons]


def main():
    jettons = merge_jettons()
    jettons_md = "\n".join(["[%s](https://tonapi.io/jetton/%s) | %s" %(j[0], j[1], j[1]) for j in jettons])

    open('README.md', 'w').write(open("readme.md.template").read() % (jettons_md) )


if __name__ == '__main__':
    main()