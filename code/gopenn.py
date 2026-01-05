import os
import numpy
import pickle
import keras
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from dataset import Dataset
from ecisreader import EcisReader


class GOPENN:
    def __init__(self, dataset: list[Dataset]) -> None:
        self.dataset = dataset


if __name__ == '__main__':
    pass
