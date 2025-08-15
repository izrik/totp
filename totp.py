#!/usr/bin/env python3


import argparse
import os
import sys

import yaml
import mintotp

HOME = os.getenv('HOME')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument(
        '--config', '-c', default=f'{HOME}/.config/totp.yaml',
        help='Path to the config file. Defaults to "~/.config/totp.yaml".')
    parser.add_argument('-n', action='store_true')
    args = parser.parse_args()
    config_path = args.config
    with open(config_path) as f:
        config = yaml.safe_load(f)
    name = args.name.strip()
    items = config.get('items') or []
    if name == 'list':
        name_len = 0
        for item in items:
            name_len = max(name_len, len(item.get('name', '')))
        fs = f'{{0:{name_len}}} {{1}}'
        for item in items:
            print(fs.format(item.get('name', ''),
                            item.get('display_name', '')))
        return 0
    for item in items:
        if item.get('name', '') == name:
            key = item.get('key')
            otp = mintotp.totp(key)
            import time
            time_step = 30
            time_remaining = int(time_step - time.time() % time_step)
            plural = '' if time_remaining == 1 else 's'
            if args.n:
                print(f'{name}: ', file=sys.stderr)
                print(str(otp))
                print(f'Good for {time_remaining} second{plural}.', file=sys.stderr)
            else:
                print(f'{name}: {otp}')
                print(f'Good for {time_remaining} second{plural}.')
            return
    print(f'No entry found named "{name}"')
    sys.exit(1)


if __name__ == '__main__':
    main()
