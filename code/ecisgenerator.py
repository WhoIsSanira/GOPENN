import os
import numpy
from globals import *
from nuclei import Nuclei, Rutherford


class EcisGenerator:
    def __init__(self, path: str, use_globalop: bool = False) -> None:
        self.__path = path
        self.__use_globalop = use_globalop

    @property
    def path(self) -> str:
        return self.__path
    
    def generate(self, file: str) -> str:
        with open(file, "r") as text:
            buffer = text.read().split("\n")

        beam = self.find_beam(buffer)
        target = self.find_target(buffer)
        energy = self.find_energy(buffer)
        xsections = self.take_xsections(buffer)

        return self.write_down(beam, target, energy, xsections)

    def write_down(self, beam: Nuclei, target: Nuclei, energy: float, xsections: tuple[list[float]]) -> str:
        directories = os.listdir(self.__path)
        beamdir = self.__path + f"\\{beam.name}"
        if beam.name not in directories:
            os.mkdir(beamdir)

        filename = f"{target.name}+{beam.name}_{round(energy, 2)}_in.txt"
        if filename in os.listdir(beamdir):
            filename = f"{target.name}+{beam.name}_{round(energy, 2)}_in_2.txt"

        generated_file = beamdir + "\\" + filename

        content = f"{target.name} + {beam.name} = {target.name} + {beam.name} E = {round(energy, 2)} MeV\n"
        content += self.write_settings()
        content += self.write_information(beam, target, energy)
        content += self.write_opticals(beam, target, energy)
        content += self.write_xsections(xsections)
        content += "FIN"

        with open(generated_file, "w") as file:
            file.write(content)
            
        return generated_file
    
    def write_settings(self) -> str:
        settings = "TFFFFFFFFFFFFFFTFFFFFFFFTTFTFFTTFFFFFFFFFFFF\n"
        settings += "FFTTFTFFFFFFFFFFFFFFTFFTFFFFFFFFFFFFFFFFFFFF\n"
        settings += "1    30                  6\n"
        settings += "\n"

        return settings

    def write_information(self, beam: Nuclei, target: Nuclei, energy: float) -> str:
        incomes = [
            0.0,                     # target spin
            energy,                  # energy in lab
            0.0,                     # projectile spin
            float(beam.A),           # projectile mass
            float(target.A),         # target mass
            float(beam.Z * target.Z) # product of charges
        ]

        info = ""
        for inc in incomes:
            info += str(round(inc, 2)).ljust(10)

        return info + "\n0    0    0    0\n0.0\n"

    def write_opticals(self, beam: Nuclei, target: Nuclei, energy: float) -> str:
        sample = self.create_sample(beam, target, energy)

        opticals = ""
        for params in sample:
            for par in params:
                opticals += "{:.3f}".format(par).ljust(10)

            opticals += "\n"

        return opticals + "\n"
    
    def create_sample(self, beam: Nuclei, target: Nuclei, energy: float) -> list[list[float]]:
        if self.__use_globalop == False:
            sample = [
                [100.0, 1.200, 0.500], # Real Volume
                [ 20.0, 1.200, 0.500], # Imag Volume
                [  0.0,   0.0,   0.0], # Real Surface
                [ 10.0, 1.200, 0.500], # Imag Surface
                [  0.0,   0.0,   0.0], # Real SO
                [  0.0,   0.0,   0.0], # Imag SO
                [1.300,   0.0,   0.0]  # Coulomb
            ]
        else:
            gop = GlobalPotential.find_global_potential(beam, target, energy)
            if gop is None:
                self.__use_globalop = False
                self.create_sample(beam, target, energy)
            
            Vr, rv, av = gop.real_volume_depth(), gop.real_volume_radius(), gop.real_volume_diffuseness()
            Wv, rw, aw = gop.imag_volume_depth(), gop.imag_volume_radius(), gop.imag_volume_diffuseness()
            Wd, rd, ad = gop.imag_surface_depth(), gop.imag_surface_radius(), gop.imag_surface_diffuseness()
            rc = gop.coulomb_radius()

            sample = [
                [ Vr,  rv,  av],
                [ Wv,  rw,  aw],
                [0.0, 0.0, 0.0],
                [ Wd,  rd,  ad],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [ rc, 0.0, 0.0]
            ]

        return sample

    def write_xsections(self, xsections: tuple[list[float]]) -> str:
        n = len(xsections[0])
        content = "1.0".ljust(10) + "1.0".ljust(10) + "179.0".ljust(10) + "\n"
        content += "1".ljust(5) + "2".ljust(5) + "6".ljust(5) + "20".ljust(5) + "\n"
        content += "T0" + str(n).rjust(3) + "1".rjust(5) + "\n"

        for i in range(n):
            angle = xsections[0][i]
            xsec = xsections[1][i]
            unc = xsections[2][i]

            angle_str = str(round(angle, 4))
            xsec_str = str(round(xsec, 4))
            unc_str = str(round(unc, 2))

            content += " " + angle_str.ljust(9) + xsec_str.ljust(10) + unc_str.ljust(10) + "\n"

        content += "0.01".ljust(10) + "0.01".ljust(10) + "0.01".ljust(10) + "\n"
        content += "1".ljust(5) + "2".ljust(5) + "3".ljust(5) + "\n"

        return content

    def find_beam(self, buffer: list[str]) -> Nuclei:
        info = buffer[0]
        start = info.index("Projectile:")
        stop = info.index(";")
        
        return Nuclei.from_string(info[start + len("Projectile:") + 1: stop])
    
    def find_target(self, buffer: list[str]) -> Nuclei:
        info = buffer[0]
        start = info.index("target:")
        stop = info[start:].index(";")
        
        return Nuclei.from_string(info[start + len("target:") + 1: start + stop])

    def find_energy(self, buffer: list[str]) -> float:
        info = buffer[0]
        start = info.index("E =")
        stop = info.index("MeV")
        
        return float(info[start + len("E =") + 1: stop])

    def take_xsections(self, buffer: list[str]) -> tuple[list[float], list[float], list[float]]:
        start = next(i for i in range(len(buffer)) if "Angle" in buffer[i]) + 1

        angles, xsections = [], []
        for i in range(start, len(buffer)):
            incoms = buffer[i].split()

            angles.append(float(incoms[0]))
            xsections.append(float(incoms[1]))

        if "R/s" in buffer[start - 1]:
            beam = self.find_beam(buffer)
            target = self.find_target(buffer)
            energy = self.find_energy(buffer)

            ruth = Rutherford()
            xsections = (numpy.array(xsections) * ruth.cross_sections(beam, target, energy, numpy.array(angles))).tolist()

        # TODO: Put in order experimental uncertainties. Temporal solution.
        uncertainties = [10.0] * len(angles)
        return angles, xsections, uncertainties


def generate_all() -> None:
    gen = EcisGenerator(".\\ecis\\in")

    direct = ".\\xsections"
    projs = os.listdir(direct)
    projs = [direct + "\\" + proj for proj in projs]
    
    counter = 0
    for proj in projs:
        files = os.listdir(proj)
        files = [proj + "\\" + file for file in files]
        for file in files:
            gen.generate(file)
            counter += 1

    print(f"{counter} files was generated.")


if __name__ == '__main__':
    gen = EcisGenerator(".\\ecis\\v2\\in\\", use_globalop=True)

    direct = ".\\xsections\\v2\\8Li"
    
    counter = 0
    files = os.listdir(direct)
    files = [direct + "\\" + file for file in files]
    for file in files:
        gen.generate(file)
        counter += 1

    print(f"{counter} files was generated.")
