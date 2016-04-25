- Submit Job:
    - bsub -q 1nd -J SingleMuon_E2023TTI_NoPU < lxbatch.sh
    - bsub -q 1nd -J SingleMuMinus_E2023TTI_Pt_2_10_NoPU < lxbatch.sh
    - bsub -q 1nd -J SingleMuPlus_E2023TTI_Pt_2_10_NoPU < lxbatch.sh
    - bsub -q 1nd -J SingleMuPlus_E2023TTI_NoPU < lxbatch.sh
    - bsub -q 2nd -J SingleMuon_E2023TTI_PU140 < lxbatch.sh

- Check Job Status:
    - bjobs

- Access the output of a job that  status
    - bpeek

- Available queues are:
    - 8nm (8 minutes)
    - 1nh (1 hour)
    - 8nh
    - 1nd (1day)
    - 2nd
    - 1nw (1 week)
    - 2nw

