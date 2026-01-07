import os
import numpy
from nuclei import Nuclei


class EcisReader:
    def __init__(self):
        pass

    def read(self, file: str) -> tuple[numpy.ndarray, numpy.ndarray]:
        with open(file, 'r') as txt:
            buffer = txt.read().split('\n')

        proj = self.read_projectile(buffer)
        targ = self.read_target(buffer)
        ener = self.read_energy(buffer)
        opts = self.read_optical_parameters(buffer)

        return (numpy.array([proj[0], proj[1], targ[0], targ[1], ener]), numpy.array(opts))

    def read_projectile(self, buffer: list[str]) -> tuple[int, int]:
        start = buffer[0].index('+')
        stop = buffer[0].index('=')
        proj = Nuclei.from_string(buffer[0][start+1:stop].strip())
        return (proj.Z, proj.A)

    def read_target(self, buffer: list[str]) -> tuple[int, int]:
        stop = buffer[0].index('+')
        targ = Nuclei.from_string(buffer[0][:stop])
        return (targ.Z, targ.A)

    def read_energy(self, buffer: list[str]) -> float:
        start = buffer[0].index('E =')
        stop = buffer[0].index('MeV')
        return float(buffer[0][start+len('E ='):stop].strip())

    def read_optical_parameters(self, buffer: list[str]) -> list[float]:
        starting_index, stopping_index = 8, 15
        params = []

        for i in range(starting_index, stopping_index):
            V, r, a = buffer[i].split()
            V, r, a = float(V), float(r), float(a)
            
            if V > 0.0: params.append(V)
            if r > 0.0: params.append(r)
            if a > 0.0: params.append(a)

        return params


if __name__ == '__main__':
    pass
