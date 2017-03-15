from abc import ABCMeta, abstractmethod


class BaseModel(metaclass=ABCMeta):
    def init_data(self, data):
        self._data = data

    @abstractmethod
    def solve(self):
        pass


class Model(BaseModel):
    def solve(self):
        pass
