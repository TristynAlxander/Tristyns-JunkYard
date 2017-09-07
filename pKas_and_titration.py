import math


PKA                                 = 6
PH                                  = 0
TOTAL_ACID_CONCENTRATION            = 1
ACID_VOLUME                         = 1
STRONG_BASE_TITRATE_VOLUME          = 0.0035
STRONG_BASE_TITRATE_CONCENTRATION   = 1



def a_fraction(pKa, pH, total_concentration):
    # pH = pKa + log(A/HA)
    # pH-pKa = log(A/HA)
    # 10^(pH-pKa) = A/HA
    # # # A + HA = total_concentration
    # # # HA = total_concentration - A
    # 10^(pH-pKa) = A/(total_concentration - A)
    # total_concentration * 10^(pH-pKa) - A * 10^(pH-pKa) = A
    # A + A * 10^(pH-pKa) = total_concentration * 10^(pH-pKa)
    # A (1 + 10^(pH-pKa)) = total_concentration * 10^(pH-pKa)
    # A = total_concentration * 10**(pH-pKa) / (1+10**(pH-pKa))
    return total_concentration * 10**(pH-pKa) / (1+10**(pH-pKa))

def ha_fraction(pKa, pH, total_concentration):
    a_concentration = a_fraction(pKa, pH, total_concentration)
    return total_concentration-a_concentration

def strong_base_titration(pKa, pH, total_acid_concentration, acid_volume, titrate_volume, titrate_concentration):
    
    # CV = CV
    new_volume = acid_volume + titrate_volume
    new_titrate_concentration = titrate_concentration * titrate_volume / new_volume
    # Add Strong Base 
    # Conjugate Base
    a_concentration         = a_fraction(pKa, pH, total_acid_concentration)
    new_a_concentration     = a_concentration + new_titrate_concentration
    # Acid 
    ha_concentration        = ha_fraction(pKa, pH, total_acid_concentration)
    if(ha_concentration < new_titrate_concentration):
        return None
    new_ha_concentration = ha_concentration - new_titrate_concentration
    
        
    return pKa + math.log(new_a_concentration/new_ha_concentration,10)

def make_titration_curve(pKas, total_acid_concentration, acid_volume, titrate_step, titrate_concentration):
    # Assumes pKas is ordered least to greatest
    with open('titration_curve.txt', 'w+') as f:
        pH = 0
        total_sum = 0
        for num in range(0,900):
            choice = pKas[0]
            for pKa in pKas:
                if(math.fabs(pH - pKa) < math.fabs(pH - choice)):
                    choice = pKa
            
            total_sum = total_sum + titrate_step
            new_pH = strong_base_titration(choice, pH, total_acid_concentration, acid_volume, titrate_step, titrate_concentration)
            if(new_pH != None):
                pH = new_pH
            else:
                print(total_sum)
                break
            
            f.write("{0}\t{1}\n".format(total_sum,pH))

pkas = [1.82,6,9.2]
make_titration_curve(pkas,TOTAL_ACID_CONCENTRATION,ACID_VOLUME,STRONG_BASE_TITRATE_VOLUME,STRONG_BASE_TITRATE_CONCENTRATION)


