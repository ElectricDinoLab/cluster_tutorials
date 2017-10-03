EXPERIMENT= #Put name of experiment, should match the name you put in the qsub script
# list of subjects
SUBJ=("subject1" "subject2" "subject3")
# for each subject
for i in 0 1 2;
	do
		# pass it to the qsub script
		declare SUBJ=${SUBJ[$i]}
		echo $SUBJ
		qsub -v EXPERIMENT=$EXPERIMENT py_cluster_tut_qsub.sh ${SUBJ}

done