# Imports for Main
if (__name__ == "__main__"):
    import os
    import sys

import re
import difflib

#PROTEASE_SITES = 

RESTRICTION_SITES = {
    "BamHI":("ggatcc","cctagg"),
    "XbaI":("tctaga","agatct"),
    "NotI":("gcggccgc","cgccggcg"),
    "XhoI":("ctcgag","gagctc")
    }
COMPLEMENTARY_NUCLEOTIDES_DNA = {
    "a":"t",
    "t":"a",
    "c":"g",
    "g":"c",
    "n":"n"
    " ":" "
    }

def get_bad_protein(prot_seq):
    print("ToDo: Make this Function.")
#def translate(dna_seq):
#def transcribe(dna_seq):
#def his_tag():
#def divide

def first_dif(string_list,ignore_set=[]):
    diffs = ""
    # Get Longest String                                                # Get Longest String
    shortest_string = string_list[0]                                    #   Assume First is Longest
    for string_item in string_list:                                     #   For each other string
        if len(string_item) < len(shortest_string):                     #   Check if it's longer
            shortest_string = string_item                               #   Update definition
    # Find First Non-Matching Character                                 # Find First Non-Matching Character
    for i,c in enumerate(shortest_string):                              #   For Parallel Characters
        common_chars =[]                                                #   Reset Character List
        for string_item in string_list:                                 #   From each String
            common_chars.append(string_item[i])                         #   Add Character
        common_chars = [char for char in common_chars if char != " "]   #   Remove Spaces
        
        if ((len(set(common_chars)) > 1) and (i not in ignore_set)):    #   If there are different characters that ought not be ignored
            diffs=diffs+"|"
        elif(len(set(common_chars)) == 0):
            diffs=diffs+" "
        else:         
            diffs=diffs+"-"
            """
            print(c)
            print(set(common_chars))
            for string_item in string_list:
                print(string_item[i-1]+string_item[i]+string_item[i+1]+string_item[i+2])
            return i                                                #   return index
            """
    return diffs
    
def get_bad_dna(dna_seq):
    dna_seq = flatten_str(dna_seq)                                                              # Make DNA Readable
    bad_sites = {}                                                                              # 
    for enzyme, sites in RESTRICTION_SITES.items():                                             # Iterate over restriction sites
        list = []                                                                               #
        # ToDo make the below a loop
        list.extend([index.start() for index in re.finditer('(?='+sites[0]+')', dna_seq)])      # Find Restriction Sites Forward/Reverse
        list.extend([index.start() for index in re.finditer('(?='+sites[1]+')', dna_seq)])      # Find Restriction Sites Reverse/Forward
        if(list != [] and list != None):                                                        # Document Finds
            bad_sites[enzyme] = list                                                            #
    return bad_sites                                                                            # Return Finds

def get_complement(dna_seq):
    #dna_seq = flatten_str(dna_seq)                                                              # Make DNA Readable
    new_dna = ""
    for n in dna_seq:
        new_dna = new_dna + COMPLEMENTARY_NUCLEOTIDES_DNA[n]
    return new_dna
    
def flatten_str(seq):
    seq = seq.lower()
    seq = seq.replace(" ","")
    seq = seq.replace("\r","")
    seq = seq.replace("\n","")
    seq = seq.replace("\t","")
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
    seq_F_his    = "atactggcggccgcatccactggtgaccacc"
    seq_F_nohis  = "atactggcggccgcactcagcctgtctacctcc"
    seq_R = "ctaacatttcagaacgtttacgtcgattactgagctcagtcccg"
    
#print(first_dif([seq_wt,seq_v1,seq_vPS],ignore_list))
#print("Seq D:   "+get_complement(seq_Dc))


