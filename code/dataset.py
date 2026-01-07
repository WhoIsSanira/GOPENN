from __future__ import annotations

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
    
    @staticmethod
    def gather(path: str) -> list[Dataset]:
        ecr = EcisReader()
        datasets = []
        ecises = []

        stack = os.listdir(path)
        stack = [path + '\\' + stack[i] for i in range(len(stack))]

        while len(stack) != 0:
            current = stack.pop()

            if os.path.isfile(current):
                ecises.append(current)

            if os.path.isdir(current):
                inside = os.listdir(current)
                inside = [current + '\\' + inside[i] for i in range(len(inside))]
                stack.extend(inside)

        for j in range(len(ecises)):
            inputs, outputs = ecr.read(ecises[j])
            datasets.append(Dataset(inputs, outputs))
            print(ecises[j])

        return datasets


if __name__ == "__main__":
    Dataset.gather('ecis\\v1\\in')
