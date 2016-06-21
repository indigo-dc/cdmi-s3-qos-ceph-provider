"""
Copyright 2016 Poznan Supercomputing and Networking Center

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0
"""

import json
import configparser
import os
import argparse
import subprocess
import ast
Config = None


class Profile:

    def get_metadata(self):
        metadata = {}

        cdmi_latency = self.get_cdmi_latency()
        metadata["cdmi_latency"] = str(cdmi_latency)

        cdmi_geographic_placement = self.get_cdmi_geographic_placement()
        metadata["cdmi_geographic_placement"] = cdmi_geographic_placement

        cdmi_data_redundancy = self.get_cdmi_data_redundancy()
        metadata["cdmi_data_redundancy"] = str(cdmi_data_redundancy)

        return metadata

    def get_cdmi_latency(self):
        global Config
        return Config[self.name]["cdmi_latency"]

    def get_cdmi_data_redundancy(self):
        command = "ceph osd pool get "+self.pools[0]+" size"
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return int(output.stdout.readline()[6:-1])


    def get_cdmi_geographic_placement(self):
        global Config
        string = Config[self.name]["cdmi_geographic_placement"]
        return [chunk.strip(None) for chunk in string.split(',')]

    def __init__(self, name, values):
        self.name = name
        self.pools = ast.literal_eval(Config.get(self.name, "pools"))
        self.type = values["type"]
        self.allowed_profiles = []
        self.metadata = self.get_metadata()
        

def read_config():
    global Config
    Config = configparser.ConfigParser()
    dirname, filename = os.path.split(os.path.abspath(__file__))
    Config.read(dirname+os.sep+"profile_config.ini")


def get_profiles_names():
    global Config
    return Config.sections()


def get_profiles():
    global Config
    profiles = []
    profiles_names = get_profiles_names()
    for p in profiles_names:
        single_profile = Profile(p, Config[p])
        profiles.append(single_profile.__dict__)
    return profiles

def get_profile(profiles, bucket_name):
    profile = None
    command = "radosgw-admin bucket stats --bucket=\""+str(bucket_name)+"\""
    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    json_output = json.load(output)
    pool_name = json_output["pool"]
    for p in profiles:
        if pool_name in p["pools"]:
            profile = p

    return profile

def main():
    try:
        parser = argparse.ArgumentParser(description='Returns capabilities information from CEPH server')
        parser.add_argument('-b', '--bucket', type=str, help='Get profile of given bucket', required=False)
        parser.add_argument('-a', '--all', help='Get all profiles',action="store_true", required=False, default=False)
        args = parser.parse_args()

        if args.all:
            read_config()
            profiles = get_profiles()
            if len(profiles) ==0:
                return -1
            print(json.dumps(profiles))
        elif args.bucket:
            read_config()
            profiles = get_profiles()
            profile = get_profile(profiles, args.bucket)
            if len(profiles) ==0 and profile!=None:
                return -1
            print(json.dumps(profile))
        else:
            parser.print_help()
    except Exception as e:
        print("OS error: {0}".format(e))
        return -1

if __name__ == "__main__":
    main()
