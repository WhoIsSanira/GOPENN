import math


PROTON_NUCLONS = 1
PROTON_CHARGE = 1

DEUTERON_NUCLONS = 2
DEUTERON_CHARGE  = 1

HELIUM3_NUCLONS = 3
HELIUM3_CHARGE = 2

ALPHA_NUCLONS = 4
ALPHA_CHARGE = 2

LITHIUM6_NUCLONS = 6
LITHIUM6_CHARGE = 3

LITHIUM7_NUCLONS = 7
LITHIUM7_CHARGE = 3

LITHIUM8_NUCLONS = 8
LITHIUM8_CHARGE = 3

BERYLLIUM9_NUCLONS = 9
BERYLLIUM9_CHARGE = 4


class Printer:
    def __init__(self):
        pass

    def show(self, params: list[float], labels: list[str], title: str = 'Global Optical Pontial Parameters', step: int = 16) -> None:
        if len(params) != len(labels):
            print('No. of parameters and No. of labels must match!')
            return

        parameters = '—' * (step * len(params)) + '\n'
        parameters += '|' + title.center(step * len(params) - 1) + '|\n'
        parameters += '—' * (step * len(params)) + '\n'

        parameters += '|'

        for i in range(len(labels)):
            parameters += labels[i].center(step - 1) + '|'

        parameters += '\n'
        parameters += '—' * (step * len(params))
        parameters += '\n'

        parameters += '|'

        for i in range(len(params)):
            parameters += f'{round(params[i], 3)}'.center(step - 1) + '|'

        print(parameters)


class VarnerProton:
    def __init__(self, target_nuclons: int, target_charge: int, energy: float) -> None:
        self.at = target_nuclons
        self.zt = target_charge
        self.energy = energy

        self.params = {
            'V0'  :  52.90, # MeV
            'Vt'  :  13.10, # MeV
            'Ve'  : -0.299, # MeV
            'r0'  :  1.250, # fm
            'r00' : -0.225, # fm
            'a0'  :  0.690, # fm
            'rc'  :  1.240, # fm
            'rc0' :  0.120, # fm
            'Vso' :  5.900, # MeV
            'rso' :  1.340, # fm
            'rso0': -1.200, # fm
            'aso' :  0.630, # fm
            'Wv0' :  7.800, # MeV
            'Wve0':  35.00, # MeV
            'Wvew':  16.00, # MeV
            'Ws0' :  10.00, # MeV
            'Wst' :  18.00, # MeV
            'Wse0':  36.00, # MeV
            'Wsew':  37.00, # MeV
            'rw'  :  1.330, # fm
            'rw0' : -0.420, # fm
            'aw'  :  0.690  # fm
        }

    @property
    def coulomb_correction(self) -> float:
        e2 = 1.44 # MeV * fm
        return (6 * self.zt * PROTON_CHARGE * e2) / (5 * self.coulomb_radius() * (math.pow(self.at, 1/3) + math.pow(PROTON_NUCLONS, 1/3))) # MeV
    
    def __call__(self) -> None:
        Vr = self.real_volume_depth()
        rv = self.real_radius()
        av = self.real_diffuseness()
        Wr = self.imag_volume_depth()
        Wd = self.imag_surface_depth()
        rw = self.imag_volume_radius()
        aw = self.imag_diffuseness()
        rc = self.coulomb_radius()

        params = [   Vr,       rv,       av,       Wr,       Wd,       rw,       aw,       rc   ]
        labels = ['V real', 'r real', 'a real', 'W volu', 'W surf', 'r imag', 'a imag', 'r coul']

        printer = Printer()
        printer.show(params, labels, title='Global Optical Model paramaters for p')

    def real_volume_depth(self) -> float:
        V0, Vt, Ve = self.params['V0'], self.params['Vt'], self.params['Ve']
        return V0 + Vt * (self.at - 2 * self.zt) / self.at + Ve * (self.energy - self.coulomb_correction)
    
    def imag_volume_depth(self) -> float:
        Wv0, Wve0, Wvew = self.params['Wv0'], self.params['Wve0'], self.params['Wvew']
        return Wv0 * math.pow(1 + math.exp((Wve0 - (self.energy - self.coulomb_correction)) / Wvew), -1)

    def imag_surface_depth(self) -> float:
        Ws0, Wst, Wse0, Wsew = self.params['Ws0'], self.params['Wst'], self.params['Wse0'], self.params['Wsew']
        return (Ws0 + Wst * (self.at - 2 * self.zt) / self.at) * math.pow(1 + math.exp(((self.energy - self.coulomb_correction) - Wse0) / Wsew), -1)

    def real_radius(self) -> float:
        return self.__radius(self.params['r0'], self.params['r00'])

    def imag_volume_radius(self) -> float:
        return self.__radius(self.params['rw'], self.params['rw0'])
    
    def imag_surface_radius(self) -> float:
        return self.__radius(self.params['rw'], self.params['rw0'])
    
    def coulomb_radius(self) -> float:
        return self.__radius(self.params['rc'], self.params['rc0'])

    def real_diffuseness(self) -> float:
        return self.params['a0']

    def imag_diffuseness(self) -> float:
        return self.params['aw']

    def __radius(self, ri: float, ri0: float) -> float:
        return (ri * math.pow(self.at, 1/3) + ri0) / (math.pow(self.at, 1/3) + math.pow(PROTON_NUCLONS, 1/3))
    

class ZhangDeuteron:
    def __init__(self, at: int, zt: int, energy: float) -> None:
        self.at = at # Nuclons of Target
        self.zt = zt # Charge of Target
        self.energy = energy # Proj. energy

        self.params = {
            'Vr'  :  98.90, # MeV
            'Ve'  : -0.279, # MeV
            'rc'  :  1.300, # fm
            'rr'  :  1.110, # fm
            'rr0' : -0.167, # fm
            'rre' :  0.001, # fm
            'ar'  :  0.776, # fm
            'Wv0' :  11.50, # MeV
            'Ws0' :  7.560, # MeV
            'rw'  :  0.561, # fm
            'rw0' :  3.070, # fm
            'rwe' : -0.004, # fm
            'aw'  :  0.744, # fm
            'Wve0':  18.10, # MeV
            'Wvew':  5.970, # MeV
            'Wse0':  14.30, # MeV
            'Wsew':  4.550  # MeV
        }
    
    @property
    def coulomb_correction(self) -> float:
        e2 = 1.44 # MeV * fm
        return (6 * self.zt * DEUTERON_CHARGE * e2) / (5 * self.params['rc'] * math.pow(self.at, 1/3)) # MeV
    
    def __call__(self) -> None:
        Vr = self.real_volume_depth()
        Wr = self.imag_volume_depth()
        Wd = self.imag_surface_depth()
        rv = self.real_radius()
        rw = self.imag_radius()
        rc = self.coulomb_radius()
        av = 0.776
        aw = 0.744

        params = [   Vr,       rv,       av,       Wr,       Wd,       rw,       aw,       rc   ]
        labels = ['V real', 'r real', 'a real', 'W volu', 'W surf', 'r imag', 'a imag', 'r coul']

        printer = Printer()
        printer.show(params, labels, title='Global Optical Model paramaters for d')

    def real_volume_depth(self) -> float:
        Vr, Ve = self.params['Vr'], self.params['Ve']
        return Vr + Ve * (self.energy - self.coulomb_correction) # MeV

    def imag_volume_depth(self) -> float:
        Wv0, Wve0, Wvew = self.params['Wv0'], self.params['Wve0'], self.params['Wvew']
        return Wv0 / (1 + math.exp((Wve0 - (self.energy - self.coulomb_correction)) / Wvew)) # MeV

    def imag_surface_depth(self) -> float:
        Ws0, Wse0, Wsew = self.params['Ws0'], self.params['Wse0'], self.params['Wsew']
        return Ws0 / (1 + math.exp(((self.energy - self.coulomb_correction) - Wse0) / Wsew)) # MeV
    
    def real_radius(self) -> float:
        return self.__radius(self.params['rr'], self.params['rr0'], self.params['rre'])

    def imag_volume_radius(self) -> float:
        return self.__radius(self.params['rw'], self.params['rw0'], self.params['rwe'])
    
    def imag_surface_radius(self) -> float:
        return self.__radius(self.params['rw'], self.params['rw0'], self.params['rwe'])

    def coulomb_radius(self) -> float:
        rc = self.params['rc']
        return rc * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(self.zt, 1/3))

    def real_diffuseness(self) -> float:
        return self.params['ar']

    def imag_volume_diffuseness(self) -> float:
        return self.params['aw']
    
    def imag_surface_diffuseness(self) -> float:
        return self.params['aw']

    def __radius(self, ri: float, ri0: float, rie: float) -> float:
        return (ri * math.pow(self.at, 1/3) + ri0 + rie * (self.energy - self.coulomb_correction)) / (math.pow(self.at, 1/3) + math.pow(DEUTERON_NUCLONS, 1/3))
    

class DaehnickDeuteron:
    def __init__(self, target_nuclons: int, target_charge: int, energy: float) -> None:
        self.at = target_nuclons
        self.zt = target_charge
        self.energy = energy
        
        self.magics = [8, 20, 28, 50, 82, 126]
        self.params = {
            'V0' :  86.00,
            'Ve' : -0.285,
            'Vt' :  0.880,
            'rr' :  1.200,
            'ar' :  0.755,
            'Wv0':  15.90,
            'Ws0':  15.00,
            'E0' :  91.70,
            'rw' :  1.310,
            'aw0':  0.495,
            'awt':  0.064,
            'aws': -0.052,
            'rc' :  1.300,
        }

    def __call__(self) -> None:
        Vr = self.real_volume_depth()
        rv = self.real_radius()
        av = self.real_diffuseness()
        Wr = self.imag_volume_depth()
        Wd = self.imag_surface_depth()
        rw = self.imag_radius()
        aw = self.imag_diffuseness()
        rc = self.coulomb_radius()
        
        params = [   Vr,       rv,       av,       Wr,       Wd,       rw,       aw,       rc   ]
        labels = ['V real', 'r real', 'a real', 'W volu', 'W surf', 'r imag', 'a imag', 'r coul']

        printer = Printer()
        printer.show(params, labels, title='Global Optical Model paramaters for d')

    def real_volume_depth(self) -> float:
        V0, Ve, Vt = self.params['V0'], self.params['Ve'], self.params['Vt']
        return V0 + Ve * self.energy + Vt * self.zt * math.pow(self.at, -1/3)
    
    def imag_volume_depth(self) -> float:
        Wv0 = self.params['Wv0']
        return Wv0 * (1 - math.exp(self.__alpha()))

    def imag_surface_depth(self) -> float:
        Ws0 = self.params['Ws0']
        return Ws0 * math.exp(self.__alpha())

    def real_radius(self) -> float:
        rr = self.params['rr']
        return rr * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(DEUTERON_NUCLONS, 1/3))

    def imag_volume_radius(self) -> float:
        rw = self.params['rw']
        return rw * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(DEUTERON_NUCLONS, 1/3))
    
    def imag_surface_radius(self) -> float:
        rw = self.params['rw']
        return rw * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(DEUTERON_NUCLONS, 1/3))

    def coulomb_radius(self) -> float:
        rc = self.params['rc']
        return rc * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(DEUTERON_NUCLONS, 1/3))

    def real_diffuseness(self) -> float:
        return self.params['ar']

    def imag_volume_diffuseness(self) -> float:
        aw0, awt, aws = self.params['aw0'], self.params['awt'], self.params['aws']
        return aw0 + awt * math.pow(self.at, 1/3) + aws * sum([math.exp(-math.pow((m + self.zt - self.at) / 2, 2)) for m in self.magics])
    
    def imag_surface_diffuseness(self) -> float:
        aw0, awt, aws = self.params['aw0'], self.params['awt'], self.params['aws']
        return aw0 + awt * math.pow(self.at, 1/3) + aws * sum([math.exp(-math.pow((m + self.zt - self.at) / 2, 2)) for m in self.magics])

    def __alpha(self) -> float:
        return -math.pow(self.energy / self.params['E0'], 2)
    

class PangHelium3:
    def __init__(self, target_nuclons: int, target_charge: int, energy: float) -> None:
        self.at = target_nuclons
        self.zt = target_charge
        self.energy = energy

        self.params = {
            'V0'  :  118.3, # MeV
            'Ve'  : -0.130, # MeV
            'r0'  :  1.300, # fm
            'r00' : -0.480, # fm
            'a0'  :  0.820, # fm
            'Wv0' :  38.50, # MeV
            'Wve0':  156.1, # MeV
            'Wvew':  52.40, # MeV
            'Ws0' :  35.00, # MeV
            'Wst' :  34.20, # MeV
            'Wse0':  30.80, # MeV
            'Wsew':  106.4, # MeV
            'rw'  :  1.310, # fm
            'rw0' : -0.130, # fm
            'aw'  :  0.840, # fm
            'rc'  :  1.240, # fm
            'rc0' :  0.120  # fm
        }

    @property
    def coulomb_correction(self) -> float:
        e2 = 1.44 # MeV * fm
        return (6 * self.zt * HELIUM3_CHARGE * e2) / (5 * self.coulomb_radius() * (math.pow(self.at, 1/3) + math.pow(HELIUM3_NUCLONS, 1/3))) # MeV
    
    def __call__(self) -> None:
        Vr = self.real_volume_depth()
        rv = self.real_radius()
        av = self.real_diffuseness()
        Wr = self.imag_volume_depth()
        Wd = self.imag_surface_depth()
        rw = self.imag_radius()
        aw = self.imag_diffuseness()
        rc = self.coulomb_radius()
        
        params = [   Vr,       rv,       av,       Wr,       Wd,       rw,       aw,       rc   ]
        labels = ['V real', 'r real', 'a real', 'W volu', 'W surf', 'r imag', 'a imag', 'r coul']

        printer = Printer()
        printer.show(params, labels, title='Global Optical Model paramaters for 3He')

    def real_volume_depth(self) -> float:
        V0, Ve = self.params['V0'], self.params['Ve']
        return V0 + Ve * (self.energy - self.coulomb_correction)

    def imag_volume_depth(self) -> float:
        Wv0, Wve0, Wvew = self.params['Wv0'], self.params['Wve0'], self.params['Wvew']
        return Wv0 * math.pow(1 + math.exp((Wve0 - (self.energy - self.coulomb_correction)) / Wvew), -1)

    def imag_surface_depth(self) -> float:
        Ws0, Wst, Wse0, Wsew = self.params['Ws0'], self.params['Wst'], self.params['Wse0'], self.params['Wsew']
        return (Ws0 + Wst * (self.at - 2 * self.zt) / self.at) * math.pow(1 + math.exp(((self.energy - self.coulomb_correction) - Wse0) / Wsew), -1)

    def real_radius(self) -> float:
        return self.__radius(self.params['r0'], self.params['r00'])

    def imag_volume_radius(self) -> float:
        return self.__radius(self.params['rw'], self.params['rw0'])
    
    def imag_surface_radius(self) -> float:
        return self.__radius(self.params['rw'], self.params['rw0'])

    def coulomb_radius(self) -> float:
        return self.__radius(self.params['rc'], self.params['rc0'])

    def real_diffuseness(self) -> float:
        return self.params['a0']

    def imag_volume_diffuseness(self) -> float:
        return self.params['aw']
    
    def imag_surface_diffuseness(self) -> float:
        return self.params['aw']

    def __radius(self, ri: float, ri0: float) -> float:
        return (ri * math.pow(self.at, 1/3) + ri0) / (math.pow(self.at, 1/3) + math.pow(HELIUM3_NUCLONS, 1/3))
    

class SuAlpha:
    def __init__(self, target_nuclons: int, target_charge: int, energy: float) -> None:
        self.at = target_nuclons
        self.zt = target_charge
        self.energy = energy

        self.params = {
            'V0' :  175.09,
            'V1' : -0.6236,
            'V2' :  0.0006,
            'V3' :  30.000,
            'V4' : -0.2360,
            'W0' :  27.582,
            'W1' : -0.0797,
            'W2' :  48.000,
            'U0' : -4.0174,
            'U1' :  0.1409,
            'rr' :  1.3421,
            'rs' :  1.2928,
            'rv' :  1.4259,
            'ar' :  0.6578,
            'as' :  0.6359,
            'av' :  0.5587,
            'rc' :  1.3500
        }

    def __call__(self) -> None:
        Vr = self.real_volume_depth()
        rv = self.real_radius()
        av = self.real_diffuseness()
        Wr = self.imag_volume_depth()
        Wd = self.imag_surface_depth()
        rw = self.imag_volume_radius()
        aw = self.imag_volume_diffuseness()
        rd = self.imag_surface_radius()
        ad = self.imag_surface_diffuseness()
        rc = self.coulomb_radius()

        params = [   Vr,       rv,       av,       Wr,          rw,           aw,          Wd,          rd,            ad,         rc   ]
        labels = ['V real', 'r real', 'a real', 'W volu', 'r imag volu', 'a imag volu', 'W surf', 'r imag surf', 'a imag surf', 'r coul']

        printer = Printer()
        printer.show(params, labels, title='Global Optical Model paramaters for 4He')

    def real_volume_depth(self) -> float:
        V0, V1, V2, V3, V4 = self.params['V0'], self.params['V1'], self.params['V2'], self.params['V3'], self.params['V4']
        return V0 \
             + V1 * self.energy \
             + V2 * math.pow(self.energy, 2) \
             + V3 * (self.at - 2 * self.zt) / self.at \
             + V4 * self.zt * math.pow(self.zt, 1/3)

    def imag_volume_depth(self) -> float:
        U0, U1 = self.params['U0'], self.params['U1']
        return max(0, U0 + U1 * self.energy)

    def imag_surface_depth(self) -> float:
        W0, W1, W2 = self.params['W0'], self.params['W1'], self.params['W2']
        return max(0, W0 + W1 * self.energy + W2 * (self.at - 2 * self.zt) / self.at)

    def real_radius(self) -> float:
        rr = self.params['rr']
        return rr * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(ALPHA_NUCLONS, 1/3))

    def imag_volume_radius(self) -> float:
        rv = self.params['rv']
        return rv * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(ALPHA_NUCLONS, 1/3))

    def imag_surface_radius(self) -> float:
        rs = self.params['rs']
        return rs * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(ALPHA_NUCLONS, 1/3))

    def coulomb_radius(self) -> float:
        rc = self.params['rc']
        return rc * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(ALPHA_NUCLONS, 1/3))

    def real_diffuseness(self) -> float:
        return self.params['ar']

    def imag_volume_diffuseness(self) -> float:
        return self.params['av']

    def imag_surface_diffuseness(self) -> float:
        return self.params['as']
    

class XuLithium6:
    def __init__(self, target_nuclons: int, target_charge: int, energy: float) -> None:
        self.at = target_nuclons
        self.zt = target_charge
        self.energy = energy

        self.params = {
            'V0' :  265.74,
            'V1' : -0.1830,
            'W0' :  28.850,
            'W1' : -0.0989,
            'U0' : -5.2260,
            'U1' :  0.1180,
            'U2' : 0.00038,
            'rr' :  1.1200,
            'rs' :  1.3110,
            'rv' :  1.5370,
            'rc' :  1.6740,
            'ar' :  0.8140,
            'as' :  0.9390,
            'av' :  0.7260
        }

    def __call__(self) -> None:
        Vr = self.real_volume_depth()
        rv = self.real_radius()
        av = self.real_diffuseness()
        Wr = self.imag_volume_depth()
        Wd = self.imag_surface_depth()
        rw = self.imag_volume_radius()
        aw = self.imag_volume_diffuseness()
        rd = self.imag_surface_radius()
        ad = self.imag_surface_diffuseness()
        rc = self.coulomb_radius()

        params = [   Vr,       rv,       av,       Wr,          rw,           aw,          Wd,          rd,            ad,         rc   ]
        labels = ['V real', 'r real', 'a real', 'W volu', 'r imag volu', 'a imag volu', 'W surf', 'r imag surf', 'a imag surf', 'r coul']

        printer = Printer()
        printer.show(params, labels, title='Global Optical Model paramaters for 6Li')

    def real_volume_depth(self) -> float:
        V0, V1 = self.params['V0'], self.params['V1']
        return V0 + V1 * self.energy
    
    def imag_volume_depth(self) -> float:
        U0, U1, U2 = self.params['U0'], self.params['U1'], self.params['U2']
        return max(0, U0 + U1 * self.energy + U2 * math.pow(self.energy, 2))

    def imag_surface_depth(self) -> float:
        W0, W1 = self.params['W0'], self.params['W1']
        return max(0, W0 + W1 * self.energy)
    
    def real_radius(self) -> float:
        rr = self.params['rr']
        return rr * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM6_NUCLONS, 1/3))

    def imag_volume_radius(self) -> float:
        rv = self.params['rv']
        return rv * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM6_NUCLONS, 1/3))

    def imag_surface_radius(self) -> float:
        rs = self.params['rs']
        return rs * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM6_NUCLONS, 1/3))

    def coulomb_radius(self) -> float:
        rc = self.params['rc']
        return rc * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM6_NUCLONS, 1/3))
    
    def real_diffuseness(self) -> float:
        return self.params['ar']

    def imag_volume_diffuseness(self) -> float:
        return self.params['av']

    def imag_surface_diffuseness(self) -> float:
        return self.params['as']


class XuLithium7:
    def __init__(self, target_nuclons: int, target_charge: int, energy: float) -> None:
        self.at = target_nuclons
        self.zt = target_charge
        self.energy = energy

        self.params = {
            'V0' :  181.66,
            'V1' : -0.0255,
            'V2' :-0.00063,
            'W0' :  40.506,
            'W1' : -0.1250,
            'U0' :  11.092,
            'U1' :  0.3170,
            'U2' :-0.00022,
            'rr' :  1.1880 if self.at <= 100 else 1.238,
            'rs' :  1.1820,
            'rv' :  1.5930,
            'rc' :  1.8020,
            'ar' :  0.8520,
            'as' :  0.8690,
            'av' :  0.5980
        }

    def __call__(self) -> None:
        Vr = self.real_volume_depth()
        rv = self.real_radius()
        av = self.real_diffuseness()
        Wr = self.imag_volume_depth()
        Wd = self.imag_surface_depth()
        rw = self.imag_volume_radius()
        aw = self.imag_volume_diffuseness()
        rd = self.imag_surface_radius()
        ad = self.imag_surface_diffuseness()
        rc = self.coulomb_radius()

        params = [   Vr,       rv,       av,       Wr,          rw,           aw,          Wd,          rd,            ad,         rc   ]
        labels = ['V real', 'r real', 'a real', 'W volu', 'r imag volu', 'a imag volu', 'W surf', 'r imag surf', 'a imag surf', 'r coul']

        printer = Printer()
        printer.show(params, labels, title='Global Optical Model paramaters for 7Li')

    def real_volume_depth(self) -> float:
        V0, V1, V2 = self.params['V0'], self.params['V1'], self.params['V2']
        return V0 + V1 * self.energy + V2 * math.pow(self.energy, 2)
    
    def imag_volume_depth(self) -> float:
        U0, U1, U2 = self.params['U0'], self.params['U1'], self.params['U2']
        return max(0, U0 + U1 * self.energy + U2 * math.pow(self.energy, 2))

    def imag_surface_depth(self) -> float:
        W0, W1 = self.params['W0'], self.params['W1']
        return max(0, W0 + W1 * self.energy)
    
    def real_radius(self) -> float:
        rr = self.params['rr']
        return rr * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM7_NUCLONS, 1/3))

    def imag_volume_radius(self) -> float:
        rv = self.params['rv']
        return rv * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM7_NUCLONS, 1/3))

    def imag_surface_radius(self) -> float:
        rs = self.params['rs']
        return rs * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM7_NUCLONS, 1/3))

    def coulomb_radius(self) -> float:
        rc = self.params['rc']
        return rc * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM7_NUCLONS, 1/3))
    
    def real_diffuseness(self) -> float:
        return self.params['ar']

    def imag_volume_diffuseness(self) -> float:
        return self.params['av']

    def imag_surface_diffuseness(self) -> float:
        return self.params['as']
    

class SuLithium8:
    def __init__(self, target_nuclons: int, target_charge: int, energy: float) -> None:
        self.at = target_nuclons
        self.zt = target_charge
        self.energy = energy

        self.params = {
            'V0' :  187.62,
            'V1' : -0.5130,
            'W0' :  33.417,
            'W1' : -0.1320,
            'U0' :  12.329,
            'U1' :  0.3780,
            'rr' :  1.2320,
            'rs' :  1.4620,
            'rv' :  1.8000,
            'rc' :  1.5720,
            'ar' :  0.7860,
            'as' :  0.9200,
            'av' :  0.5270
        }

    def __call__(self) -> None:
        Vr = self.real_volume_depth()
        rv = self.real_radius()
        av = self.real_diffuseness()
        Wr = self.imag_volume_depth()
        Wd = self.imag_surface_depth()
        rw = self.imag_volume_radius()
        aw = self.imag_volume_diffuseness()
        rd = self.imag_surface_radius()
        ad = self.imag_surface_diffuseness()
        rc = self.coulomb_radius()

        params = [   Vr,       rv,       av,       Wr,          rw,           aw,          Wd,          rd,            ad,         rc   ]
        labels = ['V real', 'r real', 'a real', 'W volu', 'r imag volu', 'a imag volu', 'W surf', 'r imag surf', 'a imag surf', 'r coul']

        printer = Printer()
        printer.show(params, labels, title='Global Optical Model paramaters for 7Li')

    def real_volume_depth(self) -> float:
        V0, V1 = self.params['V0'], self.params['V1']
        return V0 + V1 * self.energy
    
    def imag_volume_depth(self) -> float:
        U0, U1 = self.params['U0'], self.params['U1'] #The U2 parameter was not in the original article
        return U0 + U1 * self.energy

    def imag_surface_depth(self) -> float:
        W0, W1 = self.params['W0'], self.params['W1']
        return W0 + W1 * self.energy
    
    def real_radius(self) -> float:
        rr = self.params['rr']
        return rr * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM8_NUCLONS, 1/3))

    def imag_volume_radius(self) -> float:
        rv = self.params['rv']
        return rv * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM8_NUCLONS, 1/3))

    def imag_surface_radius(self) -> float:
        rs = self.params['rs']
        return rs * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM8_NUCLONS, 1/3))

    def coulomb_radius(self) -> float:
        rc = self.params['rc']
        return rc * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(LITHIUM8_NUCLONS, 1/3))
    
    def real_diffuseness(self) -> float:
        return self.params['ar']

    def imag_volume_diffuseness(self) -> float:
        return self.params['av']

    def imag_surface_diffuseness(self) -> float:
        return self.params['as']


class XuBeryllium9:
    def __init__(self, target_nuclons: int, target_charge: int, energy: float) -> None:
        self.at = target_nuclons
        self.zt = target_charge
        self.energy = energy

        self.params = {
            'V0' :  268.07,
            'V1' : -0.1800,
            'V2' : -0.0009,
            'W0' :  52.149,
            'W1' : -0.1250,
            'U0' :  2.9650,
            'U1' :  0.2860,
            'rr0':  1.2000,
            'rr1':  0.0273,
            'rs' :  1.2000,
            'rv' :  1.6400,
            'rc' :  1.5560,
            'ar' :  0.7260,
            'as' :  0.8430,
            'av' :  0.6000,
        }

    def __call__(self) -> None:
        Vr = self.real_volume_depth()
        rv = self.real_radius()
        av = self.real_diffuseness()
        Wr = self.imag_volume_depth()
        Wd = self.imag_surface_depth()
        rw = self.imag_volume_radius()
        aw = self.imag_volume_diffuseness()
        rd = self.imag_surface_radius()
        ad = self.imag_surface_diffuseness()
        rc = self.coulomb_radius()

        params = [   Vr,       rv,       av,       Wr,          rw,           aw,          Wd,          rd,            ad,         rc   ]
        labels = ['V real', 'r real', 'a real', 'W volu', 'r imag volu', 'a imag volu', 'W surf', 'r imag surf', 'a imag surf', 'r coul']

        printer = Printer()
        printer.show(params, labels, title='Global Optical Model paramaters for 9Be')

    def real_volume_depth(self) -> float:
        V0, V1, V2 = self.params['V0'], self.params['V1'], self.params['V2']
        return V0 + V1 * self.energy + V2 * math.pow(self.energy, 2)
    
    def imag_volume_depth(self) -> float:
        U0, U1 = self.params['U0'], self.params['U1']
        return max(0, U0 + U1 * self.energy)

    def imag_surface_depth(self) -> float:
        W0, W1 = self.params['W0'], self.params['W1']
        return max(0, W0 + W1 * self.energy)
    
    def real_radius(self) -> float:
        rr0, rr1 = self.params['rr0'], self.params['rr1']
        return (rr0 + rr1 * math.pow(self.at, 1/3)) * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(BERYLLIUM9_NUCLONS, 1/3))

    def imag_volume_radius(self) -> float:
        rv = self.params['rv']
        return rv * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(BERYLLIUM9_NUCLONS, 1/3))

    def imag_surface_radius(self) -> float:
        rs = self.params['rs']
        return rs * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(BERYLLIUM9_NUCLONS, 1/3))

    def coulomb_radius(self) -> float:
        rc = self.params['rc']
        return rc * math.pow(self.at, 1/3) / (math.pow(self.at, 1/3) + math.pow(BERYLLIUM9_NUCLONS, 1/3))
    
    def real_diffuseness(self) -> float:
        return self.params['ar']

    def imag_volume_diffuseness(self) -> float:
        return self.params['av']

    def imag_surface_diffuseness(self) -> float:
        return self.params['as']


if __name__ == '__main__':
    lith = SuLithium8(7, 3, 11.0)
    lith()