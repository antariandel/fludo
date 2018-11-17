#!/usr/bin/env python

class Liquid:
    ''' Liquid made of PG and VG. Has volume in ml, PG in percentage and VG calculated. '''
    def __init__(self, ml, pg=50):
        if type(ml) not in [int, float]:
            raise TypeError('Volume has to be either int or float!')
        if type(pg) not in [int, float]:
            raise TypeError('PG percent has to be either int or float!')
        
        self.ml = ml
        self.pg = max(0, min(pg, 100)) # clamp to 0..100
        self.vg = 100 - self.pg
        self.total_pgml = self.ml * (self.pg / 100)
        self.total_vgml = self.ml - self.total_pgml
    
    def __str__(self):
        return '%sml Base %sPG/%sVG' % (self.ml, self.pg, self.vg)


class NicBase(Liquid):
    ''' Inherits Liquid. Adds nicotine concentration in mg/ml. '''
    def __init__(self, ml, pg=50, nic=6):
        if type(nic) not in [int, float]:
            raise TypeError('Nicotine concentration has to be either int or float!')
        
        super().__init__(ml, pg)

        self.nic = nic
        if self.nic < 0:
            raise ValueError('Nicotine concentration can not be smaller than 0!')
        
        # Calc nicotine mass
        self.total_nicmg = nic * ml


class Aroma(Liquid):
    ''' Inherits Liquid. Has name. '''
    def __init__(self, ml, pg=50, name='Unnamed'):
        if type(name) != str:
            raise TypeError('Name has to be a string!')
        
        super().__init__(ml, pg)

        self.name = name


class Recipe(Liquid):
    def __init__(self, *components):
        super().__init__(0)

        self.nic = 0
        self.total_nicmg = 0
        self.aromas_ml = {}
        self.aromas_percent = {}

        # Add liquids if got as arguments
        if components:
            for any_liquid in components:
                self.add(any_liquid)
    
    def add(self, *components):
        for component in components:
            if type(component) not in [Liquid, NicBase, Aroma, Recipe]:
                raise TypeError('Can only add Liquid, NicBase, Aroma and Mix types!')
            
            # Volume addition and PG/VG recalculation
            self.ml += component.ml
            self.total_pgml += component.total_pgml
            self.total_vgml += component.total_vgml
            if self.ml > 0:
                self.pg = (self.total_pgml / self.ml) * 100
                self.vg = 100 - self.pg
            else:
                self.pg, self.vg = 50, 50

            # NicBase only: Nicotine mass addition
            if type(component) == NicBase:
                self.total_nicmg += component.total_nicmg
            
            # Aroma only: Aroma names addition and per-aroma volume recalculation
            elif type(component) == Aroma:
                if component.name in self.aromas_ml:
                    self.aromas_ml[component.name] += component.ml
                else:
                    self.aromas_ml[component.name] = component.ml
            
            # Recipe only: Nicotine mass and aroma volume additions
            elif type(component) == Recipe:
                self.total_nicmg += component.total_nicmg
                for aroma in component.aromas_volume:
                    if aroma in self.aromas_ml:
                        self.aromas_ml[aroma] += component.aromas_ml['aroma']
                    else:
                        self.aromas_ml[aroma] = component.aromas_ml['aroma']
            
            # Recalculate nicotine concentration in total volume
            self.nic = self.total_nicmg / self.ml

            # Recalculate aromas percentage in relation to total volume
            for aroma in self.aromas_ml:
                self.aromas_percent[aroma] = (self.aromas_ml[aroma] / self.ml) * 100
        return self
    
    def pour(self, amount):
        ''' Returns amount of volume from the recipe with the same ratio of components '''
        # TODO: Create this
        pass