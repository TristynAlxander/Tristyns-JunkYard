# Imports
import os
import sys
import re
import difflib
from Bio import pairwise2

# Add Source Scripts to Path                                        # Add Source Scripts to Path
current_dir = os.path.dirname(os.path.realpath(__file__))+"/"       # Current Directory
source__dir = current_dir+"../source_scripts/"                      # Relative Position of Source
sys.path.insert(0, source__dir)                                     # Add to Path
# Source Imports
from str_functions import StringFunctions as str_f



class PrettySeq:
    def simplify_seq(seq):
        return str_f.simplify_str(seq)
    
    def dna_to_dna_frame(dna_seq,n=3):
        dna_frame = [dna_seq[i:i+n] for i in range(0, len(dna_seq), n)]
        return dna_frame
    
    def get_pretty_dna(dna_seq):
        dna_seq    = simplify_seq(dna_seq)
        dna_frame  = dna_to_dna_frame(dna_seq)
        pretty_dna = ""
        for i in dna_frame:
            pretty_dna = pretty_dna + " " + i
        return pretty_dna
        
    def get_pretty_aa(aa_seq):
        aa_seq = simplify_seq(aa_seq).upper()
        prot_list = list(aa_seq)
        pretty_prot = ""
        for i in prot_list:
            pretty_prot = pretty_prot + "   " + i
        return pretty_prot

class AnalyzeSeq:
    # Class Variables
    COMPLEMENTARY_NUCLEOTIDES_DNA = {
        "a":"t",
        "t":"a",
        "c":"g",
        "g":"c",
        "n":"n",
        " ":" "
        }
    RESTRICTION_SITES = {
        "BamHI":("ggatcc","cctagg"),
        "XbaI":("tctaga","agatct"),
        "NotI":("gcggccgc","cgccggcg"),
        "XhoI":("ctcgag","gagctc")
        }
    
    # Class Functions
    def get_bad_dna(dna_seq):
        dna_seq = simplify_seq(dna_seq)                                                             # Make DNA Readable
        bad_sites = {}                                                                              # 
        for enzyme, sites in AnalyzeSeq.RESTRICTION_SITES.items():                                  # Iterate over restriction sites
            list = []                                                                               #
            # ToDo make the below a loop
            list.extend([index.start() for index in re.finditer('(?='+sites[0]+')', dna_seq)])      # Find Restriction Sites Forward/Reverse
            list.extend([index.start() for index in re.finditer('(?='+sites[1]+')', dna_seq)])      # Find Restriction Sites Reverse/Forward
            if(list != [] and list != None):                                                        # Document Finds
                bad_sites[enzyme] = list                                                            #
        return bad_sites                                                                            # Return Finds
    #def get_bad_aa(aa_seq):
    
    #def rna_dna_protein_other 
    #def translate(na_seq):
        # Check if dna or rna
    #def transcribe(dna_seq):
    
    
    def align_str(master_seq,align__seq):
        alignments = pairwise2.align.globalxx(master_seq, align__seq)                               # Global Alignment
        str_alignments_list = []                                                                    #
        for alignment in alignments:                                                                # For each Alignment
            str_alignments_list.append(pairwise2.format_alignment(*alignment))                      # Format and Save String
        return str_alignments_list
        
    def dna_reverse_complement(dna_seq):
        new_dna = ""
        for n in dna_seq:
            new_dna = AnalyzeSeq.COMPLEMENTARY_NUCLEOTIDES_DNA[n] + new_dna
        return new_dna
    

if (__name__ == "__main__" and len(sys.argv) > 1 ):
    # sys.argv[0] is this script, so don't count it.
    
    seq = sys.argv[1]


    
#print(get_pretty_prot(seq))
#print("Seq D:   "+get_complement(seq_Dc))


