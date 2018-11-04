#!/usr/bin/env python

class Liquid:
    ''' Volume in ml, pg in percentage. '''
    def __init__(self, volume, pg=50):
        if type(volume) not in [int, float]:
            raise TypeError('Volume has to be either int or float!')
        if type(pg) not in [int, float]:
            raise TypeError('PG percent has to be either int or float!')
        self.volume = volume
        self.pg = max(0, min(pg, 100)) # clamp to 0..100
        self.vg = 100 - self.pg
        self._total_pgml = self.volume * (self.pg / 100)
        self._total_vgml = self.volume - self._total_pgml
    
    def add(self, liquid):
        if type(liquid) != Liquid:
            raise TypeError('Can only add Liquid types to Liquid!')
        self.volume += liquid.volume
        if self.volume <= 0:
            raise ValueError('Volume has to be greater than 0!')
        self._total_pgml += liquid._total_pgml
        self._total_vgml += liquid._total_vgml
        self.pg = (self._total_pgml / self.volume) * 100
        self.vg = 100 - self.pg
        return self


class NicBase(Liquid):
    ''' Concentration in mg/ml '''
    def __init__(self, volume, pg=50, nic=6):
        if type(nic) not in [int, float]:
            raise TypeError('Nic has to be either int or float!') 
        super().__init__(volume, pg)
        self.nic = nic
        if self.nic < 0:
            raise ValueError('Nicotine concentration can not be smaller than 0!')
        self._total_nicmg = nic * volume


class Aroma(Liquid):
    def __init__(self, volume, pg=50, name='aroma'):
        if type(name) != str:
            raise TypeError('Name has to be a string!')
        super().__init__(volume, pg)
        self.name = name


class Recipe(Liquid):
    def __init__(self, volume=0, pg=50):
        super().__init__(volume, pg)
        self.nic = 0
        self._total_nicmg = 0
        self.aromas_volume = {}
        self.aromas_percent = {}
    
    def add(self, any_liquid):
        if type(any_liquid) not in [Liquid, NicBase, Aroma, Recipe]:
            raise TypeError('Can only add Liquid, NicBase, Aroma and Mix types!')
        super().add(any_liquid)
        if type(any_liquid) == NicBase:
            self._total_nicmg += any_liquid.nic * any_liquid.volume
        elif type(any_liquid) == Aroma:
            if any_liquid.name in self.aromas_volume:
                self.aromas_volume[any_liquid.name] += any_liquid.volume
            else:
                self.aromas_volume[any_liquid.name] = any_liquid.volume
        elif type(any_liquid) == Recipe:
            self._total_nicmg += any_liquid.nic * any_liquid.volume
            for aroma in any_liquid.aromas_volume:
                if aroma in self.aromas_volume:
                    self.aromas_volume[aroma] += any_liquid.aromas_volume['aroma'].volume
                else:
                    self.aromas_volume[aroma] = any_liquid.aromas_volume['aroma'].volume
        self.nic = self._total_nicmg / self.volume
        for aroma in self.aromas_volume:
            self.aromas_percent[aroma] = (self.aromas_volume[aroma] / self.volume) * 100
        return self