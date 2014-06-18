#
# Copyright (c) 2014 michael presutti.
# All rights reserved.
# 
# Redistribution and use in source and binary forms are permitted
# provided that the above copyright notice and this paragraph are
# duplicated in all such forms and that any documentation,
# advertising materials, and other materials related to such
# distribution and use acknowledge that the software was developed
# by the <organization>. The name of the
# <organization> may not be used to endorse or promote products derived
# from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
#FauxCrypt processing
"""
    This is an attempt at a python implementation of the FauxCrypt algorithm
    developed by D. M. Gualtieri <gualtieri TA ieee.org>.
    Visit http://www D0T fauxcrypt D0T org/ for more info.
    
    FauxCrypt is a method of obfuscation that makes plain text easy for
    a human (English speaking human) to decipher but difficult for a machine/bot to parse.
     
    In this revision FuaxPi
    1: First and last letters of words remain where they are (this includes non alpha chars).
    2: Digraphs are swapped (at -> ta) 
    3: Consonants found in the risers list are swapped with the danglers list.
    
    TODO:
    Handle special words such as the -> teh
    Shift vowels rules.
"""

import re
import sys
import argparse

VER = sys.version_info[:2]
if VER < (3,0):
    raise RuntimeError("This module requires Python v3.0 or greater")


digraphs = ["th", "he",  "in",
            "er", "an",  "re",
            "nd", "at",  "on",
            "nt", "ha",  "es",
            "st", "en",  "ed",
            "to", "it",  "ou",
            "ea", "hi",  "is",
            "or", "ti",  "as",
            "te", "et",  "ng",
            "of"]

risers =    ['b', 'd', 'f',
             'h', 'k', 'l',
             't']

danglers =  ['g', 'j', 'p',
             'q', 'y']

prefixchr = re.compile("^\W+")
suffixchr = re.compile("\W+\s*$")

def do_danglers(word):
    r=0
    d=0
    wrd = list(word)
    for r in range(len(word)):        
        if wrd[r] in risers:
            for d in range(r,len(wrd)):
                if wrd[d] in danglers:
                    wrd[d],wrd[r] = wrd[r],wrd[d]

    return ''.join(wrd)                    

def do_digraphs(word):
    if len(word)>1:
        for digraph in digraphs:
            word=word.replace(digraph,digraph[::-1])            
    return word

def do_crypt(orig):
    word = str.strip(orig.lower())
    if word.__len__()>2:
        #Isolate first char + any non-alpha chars such as " ` etc
        #Isolate last char + any non-alpha or white space chars.
        fr=0
        bk=0
        frm = prefixchr.search(word)
        bkm = suffixchr.search(word)
        if frm:
            fr=frm.group().__len__()
            
        if bkm:
            bk=bkm.group().__len__()
            
        target = word[1+fr:-1-bk]
        target = do_digraphs(target)
        target = do_danglers(target)
        word= word[:1+fr]+target+word[-1-bk:]
    return word

            
if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("-srcfile", help="Source file to obfuscate")
    parser.add_argument("-destfile",help="Obfuscated file")
    _destfile=""
    _srcfile=""
    
    args = parser.parse_args()
    try:
        _srcfile= open(args.srcfile)
        if args.destfile:
            _destfile= open(args.destfile,'w')
            
    except:
        print("There was a problem opening source file")
        sys.exit(3)
        
    for line in _srcfile:
        fauxline = line
        for word in line.split():
            crypted=do_crypt(word)
            fauxline=fauxline.replace(word,crypted)
        
        if _destfile:
            _destfile.write(fauxline)
 
        else:
            print(fauxline)
    
    _srcfile.close()
