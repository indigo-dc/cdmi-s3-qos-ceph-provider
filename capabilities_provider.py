import json

class profile:
    def __init__(self, name, allowed_profiles, metadata):
        self.name = name
        self.type = "container"
        self.allowed_profiles = allowed_profiles
        self.metadata = metadata

def main():
    profiles = []
    metadata1 = {"cdmi_latency": "300", "cdmi_geographic_placement": ["PL","GB"], "cdmi_data_redundancy": "10"}
    metadata2 = {"cdmi_latency": "1", "cdmi_geographic_placement": ["RU","FR"], "cdmi_data_redundancy": "2"}
    profile1 = profile("profil1", [], metadata1)
    profile2 = profile("profil2", [], metadata2)
    profiles.append(profile1.__dict__)
    profiles.append(profile2.__dict__)

    print(json.dumps(profiles))

if __name__ == "__main__":
    main()
