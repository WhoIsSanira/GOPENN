import os
import numpy


class Dataset:
    def __init__(self, xs: numpy.ndarray, ys: numpy.ndarray) -> None:
        self.__xs = xs
        self.__ys = ys

    @property
    def xs(self) -> numpy.ndarray:
        return self.__xs.copy()
    
    @property
    def ys(self) -> numpy.ndarray:
        return self.__ys.copy()
    

def gather(path: str) -> list[Dataset]:
    files = os.listdir(path)
    for i in range(len(files)):
        if os.path.isdir(files[i]):
            subfiles = os.listdir(files[i])



if __name__ == "__main__":
    pass
