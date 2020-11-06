python copyMadgraphGridpackToEOS.py --MGversion V5_2.6.5 --file AZhToLLTT2016-v2_08Oct2020.txt --era 2016 --version v2 --copy True
python copyMadgraphGridpackToEOS.py --MGversion V5_2.6.5 --file BBAToZhToLLTT-v2_08Oct2020.txt --era 2016 --version v2 --copy True
python copyMadgraphGridpackToEOS.py --MGversion V5_2.6.5 --file AZhToLLTT2017UL-v2_08Oct2020.txt --era 2017 --version v2 --copy True
python copyMadgraphGridpackToEOS.py --MGversion V5_2.6.5 --file BBAToZhToLLTT2017UL-v2_08Oct2020.txt --era 2017 --version v2 --copy True

python copyMadgraphGridpackToEOS.py --MGversion V5_2.6.5 --file AZhToLLTT2016-v2_08Oct2020.txt --era 2016 --version v2 --copy True >& AZhToLLTT2016-v2_cvmfs_08Oct2020.txt
python copyMadgraphGridpackToEOS.py --MGversion V5_2.6.5 --file BBAToZhToLLTT-v2_08Oct2020.txt --era 2016 --version v2 --copy True >& BBAToZhToLLTT-v2_cvmfs_08Oct2020.txt
python copyMadgraphGridpackToEOS.py --MGversion V5_2.6.5 --file AZhToLLTT2017UL-v2_08Oct2020.txt --era 2017 --version v2 --copy True >& AZhToLLTT2017UL-v2_cvmfs_08Oct2020.txt
python copyMadgraphGridpackToEOS.py --MGversion V5_2.6.5 --file BBAToZhToLLTT2017UL-v2_08Oct2020.txt --era 2017 --version v2 --copy True >& BBAToZhToLLTT2017UL-v2_cvmfs_08Oct2020.txt
