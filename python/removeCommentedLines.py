#!/usr/bin/env python

import sys
import os
import re

def removeComments(filename):

    os.system("sed -i '/^#/ d' %s"%filename)
    """
    rm_re = re.compile("\A\S*#")
    
    fIN = open(filename,"rw")
    for line in fIN:
        match = rm_re.search(line)
        if match:
            os.system("sed '%s d'"%line)
            print line
    fIN.close()
    """

def main():

    filesIn = sys.argv[1:]

    for f in filesIn:
        removeComments(f)

if __name__ == "__main__":
    main()
