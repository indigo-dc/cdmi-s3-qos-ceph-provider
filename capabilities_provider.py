import json
import configparser
import ast
Config = None


class profile:

    def get_metadata(self):
        metadata = {}

        cdmi_latency = self.get_cdmi_latency()
        metadata["cdmi_latency"] = str(cdmi_latency)

        print(type(self.get_cdmi_geographic_placement()))
        cdmi_geographic_placement = self.get_cdmi_geographic_placement()
        metadata["cdmi_geographic_placement"] = cdmi_geographic_placement

        cdmi_data_redundancy = self.get_cdmi_data_redundancy()
        metadata["cdmi_data_redundancy"] = str(cdmi_data_redundancy)

        return metadata

    def get_cdmi_latency(self):
        global Config
        return Config[self.name]["cdmi_latency"]

    def get_cdmi_data_redundancy(self):
        global Config
        return Config[self.name]["cdmi_data_redundancy"]

    def get_cdmi_geographic_placement(self):
        global Config
        string = Config[self.name]["cdmi_geographic_placement"]
        return [chunk.strip(None) for chunk in string.split(',')]

    def __init__(self, name, values):
        self.name = name
        self.type = values["type"]
        self.allowed_profiles = []
        self.metadata = self.get_metadata()


def read_config():
    global Config
    Config = configparser.ConfigParser()
    Config.read("profile_config.ini")


def get_profiles_names():
    global Config
    return Config.sections()


def get_profiles():
    global Config
    profiles = []
    profiles_names = get_profiles_names()
    for p in profiles_names:
        single_profile = profile(p, Config[p])
        profiles.append(single_profile.__dict__)
    return profiles


def main():
    read_config()
    profiles = get_profiles()
    print(json.dumps(profiles))

if __name__ == "__main__":
    main()
