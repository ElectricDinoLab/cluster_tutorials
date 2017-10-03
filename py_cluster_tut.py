#!/usr/bin/env python
# amanda szymanski @ duke university, davis lab

# python script example for use on cluster


# you need to import these as they will allow you to navigate to the proper directories and reference the subject

# time/re/datetime/smtplib aren't really needed, but you do need sys & os as these let you navigate to different directories
import sys,os,time,re,datetime,smtplib

# argparse is what lets you integrate subjects fed in from submit/qsub scripts to the python script
import argparse

# this is needed to differentiate between what kind of host you're using on the cluster
import socket


# this is where you specify what your python script is doing & what python should do
# with the subjects sent in from the submit/qsub scripts. "--subj" is a flag in the qsub
# script, which precedes the $SUBJ variable from the submit script, which is what specific subject
# needs to be passed. We take the input from "--subj" and assign it to "subjnum" in the python script.
parser = argparse.ArgumentParser(description = 'write a description of what script is doing')
parser.add_argument("--subj", dest="subjnum", help="subject id", required=True)
# args is a variable composed of the different variables from parser.add_argument. If we had multiple
# parser.add_argument commands, we'd be able to reference each variable through args.variable name. 
# in this script, we only care about the subject, so we only have args.subjnum
args = parser.parse_args()

# variable containing information on where in the cluster our data is
expname = "Folder/StudyID"
# specify which munin you're on, 1 2 or 3
muninshare = "munin#"

# sometimes scripts are run on nodes & sometimes on blades, so to ensure script runs regardless,
# you tell it that it can run on either. this is also the area where you specify what the base 
# directory is. 
thishost = socket.gethostname()
if ('node' in thishost) or ('blade' in thishost):
    basedir = os.path.join("/mnt" + "/BIAC/", muninshare + ".dhe.duke.edu/",expname)

# amico requires two directories which is set in the variable ae = amico.Evaluation(BaseDir, SubjectDir)
# aeDir1 is the base directory. it should have the folders for all relevant subjects inside it
aeDir1 = os.path.join(basedir + "/Path/to/study/directory/")
# analysisdir is each subject's directory. 
analysisdir = os.path.join(basedir + "/Path/to/study/directory/", args.subjnum)
# we also need bvecs & bvals to run NODDI. this follow the same sort of pattern as above.
bvecDir = os.path.join(analysisdir + args.subjnum + "_bvecs")
# same as above
bvalDir = os.path.join(analysisdir + args.subjnum + "_bvals")


# now we are creating the function NODDI & it has one input parameter: subject.

def NODDI(subject):
    """
    Perform NODDI analysis on each input subject.
    Takes ~ 3-4 hours per subject.
    """
    # strip subjects of empty carriage returns & quotation marks
    # ^ this is a left over from a previous iteration which had a text file of subjects. probably not necessary
    # for this cluster script, but doesn't hurt to have. 
    subject = subject.strip()
    subject = subject.strip('"')

    # tell AMICO the location/directory containing all the data for this study & subjects
    ae = amico.Evaluation(aeDir1, analysisdir)
    # create scheme file
    amico.util.fsl2scheme(bvalDir, bvecDir)
    # load the data
    ae.load_data(dwi_filename = "write whatever prefix you have that identifies your processed dwi data" + subject + ".nii.gz", scheme_filename = subject + "_bvals.scheme", mask_filename = "write whatever prefix you have that identifies your processed mask data" + subject + "_mask.nii.gz", b0_thr = 0)
    # compute the response functions, only needs to be done once per study, kernels will not be recomputed unless regenerate = True is specified
    ae.set_model("NODDI")
    ae.generate_kernels()
    # load precomputed kernels and adapt them to the scheme of the current subject:
    ae.load_kernels()
    # model fit
    ae.fit()
    # save the results as nifti images
    ae.save_results()


# need this part below to actually run the function created above
if __name__ == "__main__":
    # amico & spams are needed specifically for NODDI
    import amico
    import spams
    amico.core.setup()
    NODDI(args.subjnum)


