import json

class profile:
    def __init__(self, name, allowed_profiles, metadata):
        self.name = name
        self.type = "container"
        self.allowed_profiles = allowed_profiles
        self.metadata = metadata

def main():
    profiles = []
    metadata1 = {"latency": 300, "geographic_placement": ["PL","GB"], "data_redundancy": 10}
    metadata2 = {"latency": 1, "geographic_placement": ["RU","FR"], "data_redundancy": 2}
    profile1 = profile("profil1", [], metadata1)
    profile2 = profile("profil2", [], metadata2)
    profiles.append(profile1.__dict__)
    profiles.append(profile2.__dict__)

    print(json.dumps(profiles))
    print("OK")

if __name__ == "__main__":
    main()
