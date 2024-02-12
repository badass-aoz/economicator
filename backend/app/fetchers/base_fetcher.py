from abc import ABC, abstractmethod
import requests


class BaseFetcher(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def process_data(self, data):
        pass

    """ Consider using get_data instead of fetch_data and process_data """

    def get_data(self):
        data = self.fetch_data()
        return self.process_data(data)
