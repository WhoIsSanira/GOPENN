import os
from nuclei import Nuclei


class EcisGenerator:
    def __init__(self, path: str) -> None:
        self.__path = path

    @property
    def path(self) -> str:
        return self.__path
    
    def generate(self, file: str) -> str:
        pass

    def find_beam(self) -> Nuclei:
        pass
    
    def find_target(self) -> Nuclei:
        pass

    def find_energy(self) -> float:
        pass


if __name__ == '__main__':
    pass
