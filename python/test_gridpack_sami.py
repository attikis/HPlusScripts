#!/usr/bin/env python

import os
import sys
import subprocess

def main():

    tarballs = sys.argv[1:]
    success = []
    for tb in tarballs:
        tarball=os.path.abspath(tb)
        path = os.path.dirname(tarball)
        #output = os.path.basename(tarball).replace(".tar.xz",".out")
        output = tarball.replace(".tar.xz",".out")

#        print path
        print output

        os.mkdir("testgridpack")
        with open(os.devnull, 'wb') as devnull:
            print "Unpacking the tar ball.."
            subprocess.check_call(['tar', 'xfv',tarball, '-C','testgridpack' ], stdout=devnull, stderr=subprocess.STDOUT)

#        os.system("cd testgridpack && tar xfv %s"%tarball)
        
        os.system("grep VERSION testgridpack/gridpack_generation.log")
        #os.system("./runcmsgrid.sh 10 12345678 4 >& %s"%output)
        print "\033[98m {Running to get lhe file}\033[00m"
        os.system("cd testgridpack && ./runcmsgrid.sh 10 23212 3 >& %s"%output)
        #os.system("tail %s"%output)

        ok = "ok"
        if os.path.exists("testgridpack/cmsgrid_final.lhe") or os.path.exists("testgridpack/cmsgrid_final.lhe.gz"):
            print "LHE file found, gridpack ok"
            success.append(output)
        else:
            print "LHE file not found"
            os.system("grep error %s"%output)
            ok = "err"
        print "\033[98m"
        os.system("mv %s %s"%(output,output+"."+ok))
#        os.system("mv %s %s"%(output,os.path.join(path,output+"."+ok)))
        os.system("rm -rf testgridpack")
        os.system("echo '\e[30m'") # change font to black

    print "Gridpacks ready and ok:"
    for s in success:
        print os.path.basename(s)

if __name__ == "__main__":
    main()
