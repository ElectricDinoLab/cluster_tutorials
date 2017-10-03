# cluster_tutorials
tutorials on how to create cluster scripts (specific to Duke)

First script you need is py_cluster_tut_submit.sh, _which contains the list of subjects you want to run analyses on.
Then, qsub script receives each subject & passes it to the python script. It also contains information on where experiment directory is & where to put output files.
Each subject is passed to the python script, which runs them as they are received.
