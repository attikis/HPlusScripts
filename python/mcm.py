#!/usr/bin/env python
'''
DESCRIPTION:


USAGE:


EXAMPLE:


LAST USED:



USEFUL LINKS:
https://github.com/cms-PdmV/mcm_scripts
https://github.com/cms-PdmV/mcm_scripts/blob/master/chain_req_forcedone.py


'''

#================================================================================================ 
# Import Modules
#================================================================================================ 
import sys
import json 
# import os
# import re
# import datetime
# import time
# import getpass 
from optparse import OptionParser 

#================================================================================================ 
# Function Definitions
#================================================================================================ 
def Verbose(msg, printHeader=False):
    if not opts.verbose:
        return
    if printHeader:
        print "=== submit2condor.py:"

    if msg !="":
        print "\t", msg
    return

def GetFName():
    return __file__.replace("./", "")

def Print(msg, printHeader=True):
    fName = GetFName() #"submit2condor.py"
    if printHeader:
        print "=== ", fName
    if msg !="":
        print "\t", msg
    return

def PrintFlushed(msg, printHeader=True):
    '''
    Useful when printing progress in a loop
    '''
    msg = "\r\t" + msg
    if printHeader:
        print "=== ", GetFName()
    sys.stdout.write(msg)
    sys.stdout.flush()
    return     

def AskUser(msg, printHeader=False):
    '''
    Prompts user for keyboard feedback to a certain question.
    Returns true if keystroke is \"y\", false otherwise.
    '''
    if printHeader:
                keystroke = raw_input("=== " + GetFName() + "\n\t" +  msg + " (y/n): ")
    else:
        keystroke = raw_input("\t" +  msg + " (y/n): ")

    if (keystroke.lower()) == "y":
        return True
    elif (keystroke.lower()) == "n":
        return False
    else:
        AskUser(msg)


def main(opts):

    sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
    from rest import McM

    # Create McM instance, use default cookie location
    mcm = McM(dev=True)

    # Examples
    if 0:
        mcm.get('requests', 'PPD-RunIIWinter19PFCalib17pLHE-00001', method='get')
        mcm.get('requests', query='prepid=*-RunIIWinter19PFCalib17pLHE-*&status=new')

    validRequests = ["batches", "campaigns", "chained_campaigns", "chained_requests", 
                     "flows", "invalidations", "lists", "mccms", "requests", "users"]
 
    request = "requests"
    if request not in validRequests:
        raise Exception("Invalid request \"%s\". Please select one of the following: \"%s\"" % (request, "\", \"".join(validRequests) ) )

    # Choose Prepid of a request
    #prepid = 'PPD-RunIIWinter19PFCalib17pLHE-00001'
    prepid = 'HIG-RunIIFall18wmLHEGS-03200'
    #prepid = 'HIG-RunIIFall18wmLHEGS-*'

    # Get the request dictionary from McM with "prepid" prepid
    req = mcm.get(request, prepid, method='get')

    # Nicely print dictionary with four space indents
    if 0:
        print(json.dumps(req, indent=4))

    # Getting range of requests
    input_data = """
    B2G-Fall13-00001
    B2G-Fall13-00005 -> B2G-Fall13-00015
    """
    req = mcm.get_range_of_requests(input_data)
    if 0:
        print(json.dumps(req, indent=4))


    # Clone request
    req = mcm.get(request, "TOP-RunIISummer15wmLHEGS-00111")
    req_clone = mcm.clone_request(req)
    print(json.dumps(req_clone, indent=4))
    # Verify that they were created: https://cms-pdmv-dev.cern.ch/mcm/requests?actor=attikis&page=0&shown=63
    
    return


if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html
 
    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''

    # Default settings
    VERBOSE     = False
    DIRNAME     = None
    USERNAME    = None

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-d", "--dirName", dest="dirName", action="store", default = DIRNAME,
                      help="Name of directory to be checked for status [default: %s]" % (DIRNAME) )

    parser.add_option("-u", "--userName", dest="userName", action="store", default = USERNAME,
                      help="User name to be used for commands [default: %s]" % (USERNAME) )

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store",
                      help="List of cards to include, regex based")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store",
                      help="List of cards to exclude, regex based")

    (opts, parseArgs) = parser.parse_args()

    #  Call main functionm
    main(opts)

    # Check the status of your jobs (if any submitted)
    Verbose("Done", True)

