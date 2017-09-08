import math


PKA                                 = 6
PH                                  = -5
TOTAL_ACID_CONCENTRATION            = 1                 # Can not be negative!
ACID_VOLUME                         = 1
STRONG_BASE_TITRATE_VOLUME          = 0.0035
STRONG_BASE_TITRATE_CONCENTRATION   = 1                 # Can not be negative!



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
    
    # pH = pKa + math.log(new_a_concentration/new_ha_concentration,10)
    return pKa + math.log(new_a_concentration/new_ha_concentration,10)

def strong_acid_titration(pKa, pH, total_acid_concentration, acid_volume, titrate_volume, titrate_concentration):
    
    # CV = CV
    new_volume = acid_volume + titrate_volume
    new_titrate_concentration = titrate_concentration * titrate_volume / new_volume
    # Add Strong Base 
    # Conjugate Base
    a_concentration         = a_fraction(pKa, pH, total_acid_concentration)
    if(a_concentration < new_titrate_concentration):
        return None
    new_a_concentration     = a_concentration - new_titrate_concentration
    # Acid 
    ha_concentration        = ha_fraction(pKa, pH, total_acid_concentration)
    new_ha_concentration = ha_concentration + new_titrate_concentration
    
    # pH = pKa + math.log(new_a_concentration/new_ha_concentration,10)
    return pKa + math.log(new_a_concentration/new_ha_concentration,10)

def make_base_titration_curve(pKas, total_acid_concentration, acid_volume, titrate_step, titrate_concentration):
    # Assumes pKas is ordered least to greatest
    normalization = []
    with open('titration_curve.txt', 'w+') as f:
        pH = -5
        total_sum = 0
        my_pka = pKas[0]
        for num in range(0,900):
            
            for pKa in pKas:
                if(math.fabs(pH - pKa) < math.fabs(pH - my_pka)):
                   my_pka = pKa
                   normalization.append(total_sum + titrate_step)
            
            total_sum = total_sum + titrate_step
            new_pH = strong_base_titration(my_pka, pH, total_acid_concentration, acid_volume, titrate_step, titrate_concentration)
            
            if(new_pH != None):
                pH = new_pH
                f.write("{0}\t{1}\n".format(total_sum,pH))
            else:
                if(pKas.index(my_pka) < len(pKas)-1):
                    my_pka = pKas[pKas.index(my_pka)+1]
                    pH = strong_base_titration(my_pka, pH, total_acid_concentration, acid_volume, titrate_step, titrate_concentration)
                    f.write("{0}\t{1}\n".format(total_sum,pH))
                else:
                    break
        f.close()
    for norm in normalization:
        print(norm)
        # Pick Start of Normalization
        my_num = 0
        whole_num = math.floor(norm)
        half_num = whole_num + 0.5
        if(math.fabs(whole_num - norm) < math.fabs(half_num - norm)):
            my_num = whole_num
        else:
            my_num = half_num
        print(my_num)
        
        new_file_str = ""
        with open('titration_curve.txt', 'r') as file:
            line = file.readline()
            while(line != ""):
                tab_index = line.find("\t")
                line_number = float(line[:tab_index])
                line_end = line[tab_index:]
                if(line_number > my_num):
                    normalized_number = (line_number-my_num)*0.5/(norm-my_num)+my_num
                    if(normalized_number < my_num+0.5):
                        # Fix Line Number by Normalization
                        line_number = normalized_number
                    else:
                        # Fix Line Number by Shift
                        line_number = line_number-norm+my_num+0.5
                new_line = "{0}".format(line_number)+line_end
                new_file_str= new_file_str+new_line
                line = file.readline()
        f = open('titration_curve.txt', 'w+')
        f.write(new_file_str)
        f.close()

def make_acid_titration_curve(pKas, total_acid_concentration, acid_volume, titrate_step, titrate_concentration):
    # Assumes pKas is ordered greatest to least
    normalization = []
    with open('titration_curve.txt', 'w+') as f:
        pH = 14
        total_sum = 0
        my_pka = pKas[0]
        for num in range(0,900):
            
            for pKa in pKas:
                if(math.fabs(pH - pKa) < math.fabs(pH - my_pka)):
                   my_pka = pKa
                   normalization.append(total_sum + titrate_step)
            
            total_sum = total_sum + titrate_step
            new_pH = strong_acid_titration(my_pka, pH, total_acid_concentration, acid_volume, titrate_step, titrate_concentration)
            
            if(new_pH != None):
                pH = new_pH
                f.write("{0}\t{1}\n".format(total_sum,pH))
            else:
                if(pKas.index(my_pka) < len(pKas)-1):
                    my_pka = pKas[pKas.index(my_pka)+1]
                    print(my_pka)
                    pH = strong_acid_titration(my_pka, pH, total_acid_concentration, acid_volume, titrate_step, titrate_concentration)
                    f.write("{0}\t{1}\n".format(total_sum,pH))
                else:
                    break
        f.close()
    for norm in normalization:
        print(norm)
        # Pick Start of Normalization
        my_num = 0
        whole_num = math.floor(norm)
        half_num = whole_num + 0.5
        if(math.fabs(whole_num - norm) < math.fabs(half_num - norm)):
            my_num = whole_num
        else:
            my_num = half_num
        print(my_num)
        
        new_file_str = ""
        with open('titration_curve.txt', 'r') as file:
            line = file.readline()
            while(line != ""):
                tab_index = line.find("\t")
                line_number = float(line[:tab_index])
                line_end = line[tab_index:]
                if(line_number > my_num):
                    normalized_number = (line_number-my_num)*0.5/(norm-my_num)+my_num
                    if(normalized_number < my_num+0.5):
                        # Fix Line Number by Normalization
                        line_number = normalized_number
                    else:
                        # Fix Line Number by Shift
                        line_number = line_number-norm+my_num+0.5
                new_line = "{0}".format(line_number)+line_end
                new_file_str= new_file_str+new_line
                line = file.readline()
        f = open('titration_curve.txt', 'w+')
        f.write(new_file_str)
        f.close()


# Make Titration Curve
pkas = [-3,2]
make_base_titration_curve(pkas,TOTAL_ACID_CONCENTRATION,ACID_VOLUME,STRONG_BASE_TITRATE_VOLUME,STRONG_BASE_TITRATE_CONCENTRATION)

#ph = strong_base_titration(8.9,8.0,0.1,1,1.0e-4,1)
#print(ph)
#print(ph)

