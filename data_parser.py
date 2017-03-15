from abc import ABCMeta, abstractmethod
import json
import numpy as np


class BaseData(metaclass=ABCMeta):
    @abstractmethod
    def init_from(self, path_to_data):
        pass

    def __setattr__(self, name, value):
        """Create constant attributes"""
        if hasattr(self, name):
            raise TypeError("Can't modify data attributes")
        super().__setattr__(name, value)


class JsonData(BaseData):
    def init_from(self, json_path):
        json_file = json.load(open(json_path))
        for attr, value in json_file["Data"].items():
            self.__setattr__(attr, np.array(value, dtype=np.float64))
