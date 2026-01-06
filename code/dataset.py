import os
import numpy
from ecisreader import EcisReader


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
    ecr = EcisReader()
    datasets = []
    ecises = []

    dirs = []

    stack = os.listdir(path)
    while len(stack) != 0:
        current = stack.pop()

        full_current = path + '/' + '/'.join(dirs) + current

        if os.path.isfile(full_current):
            ecises.append(full_current)

        if os.path.isdir(full_current):
            dirs.append(current)
            stack.extend(os.listdir(path + '/' + '/'.join(dirs)))

    for j in range(len(ecises)):
        # inputs, outputs = ecr.read(ecises[j])
        # datasets.append(Dataset(inputs, outputs))
        print(ecises)

    return datasets
        

if __name__ == "__main__":
    gather('ecis/v2/in')
