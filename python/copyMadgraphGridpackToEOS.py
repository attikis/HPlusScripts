'''
USAGE:
0) First get the paths of the gridpacks
ls /afs/cern.ch/work/a/atishelm/public/gridpacks/*/* | grep 2016/ > HH_2016.txt
ls /afs/cern.ch/work/a/atishelm/public/gridpacks/*/* | grep 2017/ > HH_2017.txt

1) Then copy gridpacks and check the version of madgraph:
cp /afs/cern.ch/work/a/atishelm/public/gridpacks/gg_BulkGraviton_2017/BulkGraviton_hh_GF_HH_narrow_M1000_slc6_amd64_gcc630_CMSSW_9_3_8_tarball.tar.xz /tmp/$USER/.
cd /tmp/$USER/
tar xf *.tgz 
cat mgbasedir/VERSION

2) Once you get the MG version (e.g. 2.6.0), to check the destination.
python copyMadgraphGridpackToEOS.py --MGversion V5_2.6.0 --file HH_2016.txt

3) Ensure that year is correct (default 2017)
python copyMadgraphGridpackToEOS.py --MGversion V5_2.6.0 --file HH_2016.txt --era 2016

4) If everything is okay proceed with copying the files to cvfms
python copyMadgraphGridpackToEOS.py --file 2016.txt --MGversion V5_2.6.5 --era 2016 --copy True


LAST USED:
ls /afs/cern.ch/user/l/lcadamur/public/PerElisa_2016_gridpacks/* > 2016.txt
python copyMadgraphGridpackToEOS.py --file  2016.txt [to check MG version: copy & upack tarball & do '$cat mgbasedir/VERSION']
python copyMadgraphGridpackToEOS.py --file 2016.txt --MGversion V5_2.6.5 [change the era path to 2016]
python copyMadgraphGridpackToEOS.py --file 2016.txt --MGversion V5_2.6.5 --era 2016 --copy [make sure you get "ERROR: not existing so creating"]
python copyMadgraphGridpackToEOS.py --file 2016.txt --MGversion V5_2.6.5 --era 2016 --copy True

ls /afs/cern.ch/user/l/lcadamur/public/PerElisa_EDbEDbEDbBDCA/* >& 2017.txt


NOTE:
all files under /eos/cms/store/group/phys_generator/cvmfs/
are automatically copied by an algorithm to a replica path under
/cvmfs/cms.cern.ch/phys_generator/
which is accessible from anywhere.
For example:
/eos/cms/store/group/phys_generator/cvmfs/gridpacks/pre2017/13TeV/madgraph/V5_2.6.5/VBF_HH_CV_1_C2V_2_C3_1_13TeV-madgraph/v1/VBF_HH_CV_1_C2V_2_C3_1_13TeV-madgraph_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz
/cvmfs/cms.cern.ch/phys_generator/gridpacks/pre2017/13TeV/madgraph/V5_2.6.5/VBF_HH_CV_1_C2V_2_C3_1_13TeV-madgraph/v1/VBF_HH_CV_1_C2V_2_C3_1_13TeV-madgraph_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz
Normally the file duplication takes ~1 hour or so.


LINKS:
https://github.com/gourangakole/MCContact/blob/master/copyMadgraphGridpackToEOS_29May2019.py
https://martin-thoma.com/how-to-parse-command-line-arguments-in-python/
'''

#================================================================================================
# Import modules
#================================================================================================
import os,sys
from argparse import ArgumentParser
import ShellStyles as ShellStyles 


#================================================================================================
# Function Definition
#================================================================================================
ss = ShellStyles.SuccessStyle()
ns = ShellStyles.NormalStyle()
ts = ShellStyles.NoteStyle()
hs = ShellStyles.HighlightAltStyle()
ls = ShellStyles.HighlightStyle()
es = ShellStyles.ErrorStyle()
cs = ShellStyles.CaptionStyle()


#================================================================================================
# Function Definition
#================================================================================================
def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not args.verbose:
        return
    Print(msg, printHeader)
    return

def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return

'''
# ############ CHECK EOS PERMISSIONS ###########
# print('assign 755 to all EOS gridpack directories'); sys.stdout.flush()
# os.system('find /eos/cms/store/group/phys_generator/cvmfs/gridpacks/ -type d -exec chmod 755 {} +')
# print('assign 644 to all EOS gridpack files'); sys.stdout.flush()
# os.system('find /eos/cms/store/group/phys_generator/cvmfs/gridpacks/ -type f -exec chmod 644 {} +');
# sys.exit(1)
'''

def getBasedirByEra(era):
    baseDir = "/eos/cms/store/group/phys_generator/cvmfs/gridpacks/"
    eosDict = {}
    eosDict["2016"] = os.path.join(baseDir, "pre2017/13TeV/madgraph")
    eosDict["2017"] = os.path.join(baseDir, "2017/13TeV/madgraph")
    eosDict["2018"] = os.path.join(baseDir, "2018/13TeV/madgraph")
    eosDict["UL"]   = os.path.join(baseDir, "UL/13TeV/madgraph")

    if era in eosDict.keys():
        return eosDict[era]
    else:
        msg = "Invalid era '%s'" % (era)
        raise Exception(es + msg + ns)        

def main():

    # Retrieve the (local) path of the gridpacks from the input file
    pathList   = open(args.filename).read().splitlines()
    nGridpacks = len(pathList)
    Print("Will attempt to copy %d gridpacks to CVMFS" % (nGridpacks), True)

    # For-loop: All gridpacks
    for index, path in enumerate(pathList, 0):
        Print("%d/%d %s" % (index+1, nGridpacks, ts + path + ns), True)

        #os.system('echo '+path) # this is just for prining initial full path
	#print('stat -c "%a %n"' +path) # FIXME in future for check the permission
	gridpackname = path.split("/")[-1]
	gridpackdir  = gridpackname.split("_slc7")[0]
	version      = args.version
        basedir      = getBasedirByEra(args.era)
        MGversion    = args.mgversion
        eos_dirpath  = os.path.join(basedir,MGversion,gridpackdir,version)
        eos_path_to_copy = os.path.join(basedir,MGversion,gridpackdir,version,gridpackname)
	if (args.is4FS):
           eos_dirpath      = os.path.join(basedir,MGversion,gridpackdir,version)
           eos_path_to_copy = os.path.join(basedir,MGversion,gridpackdir,version,gridpackname)

        Verbose("eos_path_to_copy = %s" % (eos_path_to_copy), True)
	gridpack_cvmfs_path = eos_path_to_copy.replace('/eos/cms/store/group/phys_generator/cvmfs/gridpacks/','/cvmfs/cms.cern.ch/phys_generator/gridpacks/')

	Verbose("gridpack_cvmfs_path = %s" % (gridpack_cvmfs_path), True)

        # Check that the destination directory exists
	if not os.path.exists(eos_dirpath):
            cmd = 'eos mkdir -p ' + eos_dirpath
            Verbose("CVMFS directory %s does not exist" % (eos_dirpath), False)
            if(args.copy):
                Print(ss + cmd + ns, False)
                os.system(cmd)
                
        # Check that the gridpack exists
        if not os.path.isfile(eos_path_to_copy):
            cmd = 'eos cp %s %s' % (path, eos_path_to_copy)
            Verbose("CVMFS file %s does not exist" % (eos_path_to_copy), False)
            if(args.copy):
                Print(ss + cmd + ns, False)
                os.system(cmd)
        else:
            print(eos_path_to_copy)
    return

if __name__ == "__main__":

    # Default argument settings
    COPY      = False
    ERA       = "2017"
    FILE      = None
    IS4FS     = False
    MGVERSION = "V5_2.6.5"
    VERBOSE   = False
    VERSION   = "v1" # e.g /cvmfs/cms.cern.ch/phys_generator/gridpacks/pre2017/13TeV/madgraph/V5_2.6.5/AToZhToLLTT_01j_4f_M275/v1/AToZhToLLTT_01j_4f_M275_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz
    
    parser = ArgumentParser()
    
    # Add more options if you like
    parser.add_argument("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true",
                        help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE) )
    
    parser.add_argument("-f", "--file", dest="filename", metavar="FILE",
                        help="The name of the input txt file containing the location of the gridpacks to be copied [default: %s]" % (FILE) )
    
    parser.add_argument("--copy", dest="copy", default=COPY, action="store_true",
                        help="Flag that enables the copying step of the script, so that the files are transferred to EOS [default: %s]" % (COPY) )
    
    parser.add_argument("--is4FS", dest="is4FS", default=IS4FS,
                        help="Set to \"True\" if you want to make a subdir with 4FS [default: %s]" % (IS4FS) )
    
    parser.add_argument("--version", dest="version", default="v1",
                        help="The gridpack version (to be used as subdirectory in the cvmfs path) [default: %s]" % (VERSION) )
    
    parser.add_argument("--era", dest="era", default=ERA,
                        help="The era/year of collision data that the gridpack corresponds to (to be used as subdirectory in the cvmfs path) [default: %s]" % (ERA) )
    
    parser.add_argument("-MGversion", "--MGversion", dest="mgversion", default=MGVERSION,
                        help="The version of MadGraph5 (to be used as subdirectory in the cvmfs path) [default: %s]" % (MGVERSION) )

    args = parser.parse_args()

    Print("Filename ...: %s" % (args.filename) , True)
    Print("version.....: %s" % (args.version)  , False)
    Print("era.........: %s" % (args.era)      , False)
    Print("MGversion...: %s" % (args.mgversion), False)
    Print("copyToEos...: %s" % (args.copy)     , False)
    Print("is4FS.......: %s" % (args.is4FS)    , False)
    Print("Verbose ....: %s" % (args.verbose)  , False)
    
    # Sanity check: Input file
    if not os.path.isfile(args.filename):
        msg = "File '%s' not found" % (args.filename)
        raise Exception(es + msg + ns)
    else:
        msg = "The input file is %s" % (hs + args.filename + ns)
        Verbose(msg, True)
        
    # Sanity check: Era
    myEras = ["2016", "2017", "2018", "UL"]
    if args.era not in myEras:
        msg = "Unsupported era '%s'" % (args.era)
        raise Exception(es + msg + ns)
    else:
        msg = "The selected era is %s" % (hs + args.era + ns)
        Verbose(msg, True)
    
    # Call the main function
    main()
