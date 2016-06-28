import abc


class AbstractSource(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_profiles_json(self):
        pass

    @abc.abstractmethod
    def get_profile_json(self, bucket_name):
        pass