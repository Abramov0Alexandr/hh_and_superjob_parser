from abc import ABC, abstractmethod


class ParseCLS(ABC):

    @abstractmethod
    def generate_vacancy(self):
        pass

