import subprocess
import json
from profile import Profile


class DataProvider:

    def get_profiles_json(self):
        profiles = self.__get_profiles()
        if profiles is None:
            return None
        return json.dumps(profiles)

    def __get_profiles(self):
        profiles = []
        profiles_names = self.get_profiles_names()
        for p in profiles_names:
            single_profile = Profile(p, self.__config[p])
            profiles.append(single_profile.__dict__)
        if len(profiles) == 0:
            return None
        return profiles

    def get_profile_json(self, bucket_name):
        profiles = self.__get_profiles()
        profile = None
        command = "radosgw-admin bucket stats --bucket=\""+str(bucket_name)+"\""
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
        try:
            json_output = json.loads(output.decode("utf-8"))
        except ValueError:
            return json.dumps({})
        pool_name = json_output["pool"]
        for p in profiles:
            if pool_name in p["pools"]:
                profile = p
        if profile is None:
            None
        return json.dumps(profile)

    def get_profiles_names(self):
        return self.__config.sections()

    def __init__(self, config):
        self.__config = config

