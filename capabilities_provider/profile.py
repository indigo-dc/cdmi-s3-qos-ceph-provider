import ast
import subprocess


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