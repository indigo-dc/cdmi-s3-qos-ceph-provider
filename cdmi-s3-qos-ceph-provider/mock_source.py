import json
import abstract_source

class DataProvider(abstract_source.AbstractSource):

    def get_profiles_json(self):
        return "[{'metadata_provided': {'cdmi_latency_provided': '20', 'cdmi_data_redundancy_provided': '2','cdmi_geographic_placement_provided': ['PL', 'GB']},'metadata': {'cdmi_latency': '20', 'cdmi_data_redundancy': '2','cdmi_geographic_placement': ['PL', 'GB']},'pools': ['.rgw.buckets'],'type': 'container','name': 'Profile1','allowed_profiles': []},{'metadata_provided': {'cdmi_latency_provided': '300', 'cdmi_data_redundancy_provided': '2','cdmi_geographic_placement_provided': ['DE', 'CZ']},'metadata': {'cdmi_latency': '300', 'cdmi_data_redundancy': '2','cdmi_geographic_placement': ['DE', 'CZ']},'pools': ['.rgw.buckets.cdmi2'],'type': 'dataobject','name': 'Profile2','allowed_profiles': []}]"

    def get_profile_json(self, bucket_name):
        return "{'type': 'container', 'metadata': {'cdmi_geographic_placement': ['PL', 'GB'], 'cdmi_data_redundancy': '2', 'cdmi_latency': '20'}, 'name': 'Profile1', 'allowed_profiles': [], 'pools': ['.rgw.buckets']}"


    def __get_profiles_names(self):
        return self.__config.sections()

    def __init__(self, config):
        self.__config = config

