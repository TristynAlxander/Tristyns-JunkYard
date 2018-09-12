# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys

import re

RESTRICTION_SITES = {
    "BamHI":("ggatcc","cctagg"),
    "XbaI":("tctaga","agatct"),
    "XhoI":("ctcgag","gagctc")
    }
def get_bad_dna(dna_seq):
    dna_seq = flatten_str(dna_seq)                                                              # Make DNA Readable
    bad_sites = {}                                                                              # 
    for enzyme, sites in RESTRICTION_SITES.items():                                             # Iterate over restriction sites
        list = []                                                                               #
        list.extend([index.start() for index in re.finditer('(?='+sites[0]+')', dna_seq)])      # Find Restriction Sites Forward/Reverse
        list.extend([index.start() for index in re.finditer('(?='+sites[1]+')', dna_seq)])      # Find Restriction Sites Reverse/Forward
        if(list != [] and list != None):                                                        # Document Finds
            bad_sites[enzyme] = list                                                            #
    return bad_sites                                                                            # Return Finds
        
def flatten_str(seq):
    seq = seq.lower()
    seq = seq.replace(" ","")
    seq = seq.replace("\r","")
    seq = seq.replace("\n","")
    return seq
    
def get_dna_frame(dna_seq):
    n = 3
    dna_frame = [dna_seq[i:i+n] for i in range(0, len(dna_seq), n)]
    return dna_frame

def get_pretty_dna(dna_seq):
    dna_seq    = flatten_str(dna_seq)
    dna_frame  = get_dna_frame(dna_seq)
    pretty_dna = ""
    for i in dna_frame:
        pretty_dna = pretty_dna + " " + i
    return pretty_dna

def get_pretty_prot(prot_seq):
    prot_seq = flatten_str(prot_seq).upper()
    prot_list = list(prot_seq)
    pretty_prot = ""
    for i in prot_list:
        pretty_prot = pretty_prot + "   " + i
    return pretty_prot
    
if (__name__ == "__main__" and len(sys.argv) > 1 ):
    # sys.argv[0] is this script, so don't count it.
    
    seq = sys.argv[1]
else:
    seq = """
    
    """
    
print(get_bad_dna(seq))