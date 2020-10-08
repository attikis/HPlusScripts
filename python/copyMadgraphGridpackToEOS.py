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
https://martin-thoma.com/how-to-parse-command-line-arguments-in-python/
'''
#================================================================================================
# Import modules
#================================================================================================
import os,sys
from argparse import ArgumentParser

parser = ArgumentParser()

# Default argument settings
FILE      = None
VERSION   = "v1" # e.g /cvmfs/cms.cern.ch/phys_generator/gridpacks/pre2017/13TeV/madgraph/V5_2.6.5/AToZhToLLTT_01j_4f_M275/v1/AToZhToLLTT_01j_4f_M275_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz
IS4FS     = False
ERA       = "2017"
MGVERSION = "V5_2.6.0" #"V5_2.6.0"

# Add more options if you like
parser.add_argument("-f", "--file", dest="filename", metavar="FILE"
                    help="The name of the input txt file containing the location of the gridpacks to be copied [default: %s]" % (FILE) )

parser.add_argument("-copy", "--copyToEos", dest="doCopy", default=False,
                    help="make it to true if you want to really copy to EOS")

parser.add_argument("-is4FS", "--is4FS", dest="is4FS", default=IS4FS,
                    help="Set to \"True\" if you want to make a subdir with 4FS [default: %s]" % (IS4FS) )

parser.add_argument("-version", "--version", dest="version", default="v1",
                    help="The gridpack version (to be used as subdirectory in the cvmfs path) [default: %s]" % (VERSION) )

parser.add_argument("-era", "--era", dest="era", default=ERA,
                    help="The era/year of collision data that the gridpack corresponds to (to be used as subdirectory in the cvmfs path) [default: %s]" % (ERA) )

parser.add_argument("-MGversion", "--MGversion", dest="mgversion", default=MGVERSION,
                    help="The version of MadGraph5 (to be used as subdirectory in the cvmfs path) [default: %s]" % (MGVERSION) )

args = parser.parse_args()

print("Filename: " , args.filename)
print("copyToEos: ", args.doCopy)
print("is4FS: "    , args.is4FS)
print("version: "  , args.version)
print("era: "      , args.era)
print("MGversion: ", args.mgversion)

# ##############################################
# ############ CHECK EOS PERMISSIONS ###########
# ##############################################
# print('assign 755 to all EOS gridpack directories'); sys.stdout.flush()
# os.system('find /eos/cms/store/group/phys_generator/cvmfs/gridpacks/ -type d -exec chmod 755 {} +')
# print('assign 644 to all EOS gridpack files'); sys.stdout.flush()
# os.system('find /eos/cms/store/group/phys_generator/cvmfs/gridpacks/ -type f -exec chmod 644 {} +');
# sys.exit(1)
# ##############################################
# ########## END CHECK EOS PERMISSIONS #########
# ##############################################

#my_path = '/tmp/'+os.environ['USER']+'/replace_gridpacks/'

#----------------------------------------------------------------------
# main
#----------------------------------------------------------------------
#if len(sys.argv)<2:
#print "Usage: python test_copy_16Aug.py inputfile"
#	exit(0)

print "No. of args: ",len(sys.argv)
ARGV0 = sys.argv
inputFname = args.filename


# this is working
#fullgridpackpaths = open("/afs/cern.ch/user/g/gkole/work/public/abcd_v2.txt").read().splitlines()
if not( os.path.isfile(inputFname) ):
   print "WARNING!!! " + str(inputFname) + " not found!"
   exit(0)

fullgridpackpaths = open(inputFname).read().splitlines()
print "Total number of gridpack: ", len(fullgridpackpaths)

#fullgridpackpaths = [
#'/afs/cern.ch/work/w/wshi/public/MSSMD_Mneu1_60_MAD_8p5_cT_1_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz',
#'/afs/cern.ch/work/w/wshi/public/MSSMD_Mneu1_60_MAD_8p5_cT_2_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz',
#'/afs/cern.ch/work/w/wshi/public/MSSMD_Mneu1_60_MAD_8p5_cT_3_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz',
#'/eos/cms/store/user/gkole/Hgg/MC_contact/2017_gridpack/ggh/ggh012j_5f_NLO_FXFX_125_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz',
#           ]


##########################################
######## START LOOP OVER EACH GRIDPACK #########
##########################################
for fullgridpackpath in fullgridpackpaths:

        #os.system('echo '+fullgridpackpath) # this is just for prining initial full path
	#print('stat -c "%a %n"' +fullgridpackpath) # FIXME in future for check the permission
	gridpackname = fullgridpackpath.split("/")[-1]
	#print("gridpackname", gridpackname)
	gridpackdir = gridpackname.split("_slc6")[0]
	#print("gridpackdir", gridpackdir)
	version = args.version # change if needed by hand
        if (args.era == "2016"): 
           # basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc481/13TeV/madgraph'
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/pre2017/13TeV/madgraph'
        elif (args.era == "2017"):
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/2017/13TeV/madgraph'
        else:
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/2018/13TeV/madgraph'

        #MGversion = 'V5_2.4.2'
        MGversion = args.mgversion #'V5_2.6.5'

	if (args.is4FS):
           eos_dirpath = basedir+'/'+MGversion+'/4FS/'+gridpackdir+'/'+version+'/'
        else:
           eos_dirpath = basedir+'/'+MGversion+'/'+gridpackdir+'/'+version+'/'

        if (args.is4FS):
           eos_path_to_copy = basedir+'/'+MGversion+'/4FS/'+gridpackdir+'/'+version+'/'+gridpackname
        else:
           eos_path_to_copy = basedir+'/'+MGversion+'/'+gridpackdir+'/'+version+'/'+gridpackname
	#print("eos_path_to_copy", eos_path_to_copy)
	gridpack_cvmfs_path = eos_path_to_copy.replace('/eos/cms/store/group/phys_generator/cvmfs/gridpacks/','/cvmfs/cms.cern.ch/phys_generator/gridpacks/')
        os.system('echo "------------------------------------"')
	print "gridpack_cvmfs_path:  ", gridpack_cvmfs_path
	if not os.path.exists(eos_dirpath):
		print "ERROR: not existing so creating"
		print('eos mkdir -p ' + eos_dirpath);sys.stdout.flush() 
		if(args.doCopy):
			print "copy"
			os.system('eos mkdir -p ' + eos_dirpath);sys.stdout.flush()

	if not os.path.isfile(eos_path_to_copy):
		print('eos cp ' +fullgridpackpath+ ' '+eos_path_to_copy); sys.stdout.flush()
		if(args.doCopy):
			print "copy"
			os.system('eos cp ' +fullgridpackpath+ ' '+eos_path_to_copy); sys.stdout.flush()
		
        #os.system('mkdir -p '+my_path+'/'+prepid)
        #os.chdir(my_path+'/'+prepid)
        #os.system('wget -q https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/'+prepid+' -O '+prepid)
        #gridpack_cvmfs_path = os.popen('grep \/cvmfs '+prepid).read()
        #gridpack_cvmfs_path = gridpack_cvmfs_path.split('\'')[1]
	#print (gridpack_cvmfs_path)
	#os.system('tar xf '+gridpack_cvmfs_path+' -C'+my_path+'/'+prepid)
	#os.system('more '+my_path+'/'+prepid+'/'+'runcmsgrid.sh | grep "FORCE IT TO"')
	#os.system('grep _CONDOR_SCRATCH_DIR '+my_path+'/'+prepid+'/'+'mgbasedir/Template/LO/SubProcesses/refine.sh')
	#os.system('echo "------------------------------------"')
#        os.system('rm '+prepid)
##########################################
######## END LOOP OVER PREPIDS ###########
##########################################
os.system('echo "------------------------------------"')
#        gridpack_eos_path = gridpack_cvmfs_path.replace('/cvmfs/cms.cern.ch/phys_generator/gridpacks/','/eos/cms/store/group/phys_generator/cvmfs/gridpacks/')
