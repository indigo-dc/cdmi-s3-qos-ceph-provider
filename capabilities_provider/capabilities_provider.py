"""
Copyright 2016 Poznan Supercomputing and Networking Center

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0
"""

import configparser
import os
import argparse
import importlib
import sys

def read_config(name):
    config = configparser.ConfigParser()
    dir_name, filename = os.path.split(os.path.abspath(__file__))
    config.read(dir_name+os.sep+name)
    return config


def main():
    try:
        parser = argparse.ArgumentParser(description='Returns capabilities information from CEPH server')
        parser.add_argument('-b', '--bucket', type=str, help='Get profile of given bucket', required=False)
        parser.add_argument('-a', '--all', help='Get all profiles',action="store_true", required=False, default=False)
        args = parser.parse_args()

        config = read_config("config.ini")
        provider = importlib.import_module(config["Global"]["provider"])
        backend_provider = provider.DataProvider(read_config("profile_config.ini"))

        if args.all:
            profiles = backend_provider.get_profiles_json()
            if profiles is None:
                sys.exit(-1)
            print(profiles)
        elif args.bucket:
            profile = backend_provider.get_profile_json(args.bucket)
            if profile is None:
                sys.exit(-1)
            print(profile)
        else:
            parser.print_help()
    except Exception as e:
        print("OS error: {0}".format(e))
        sys.exit(-1)

if __name__ == "__main__":
    main()
