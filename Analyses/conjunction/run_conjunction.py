"""
Script to run conjunction analysis on two group-level feat 
directories for the Shared States study.
Uses the easythresh_conj script by Thomas Nichols
http://www2.warwick.ac.uk/fac/sci/statistics/staff/academic-research/nichols/
"""

from __future__ import division, print_function
import numpy as np
import nibabel as nib
import os
from glob import glob
import os.path as op

# Args
pclust = 0.05
zmin = 2.6

conj_dir = '/media/lukas/data/DecodingEmotions/Conjunction_analysis'
conj_script = '/home/lukas/Dropbox/PhD_projects/DecodingEmotions_SCAN/Analyses/easythresh_conj.sh'

zinnen_dir = '/media/lukas/data/DecodingEmotions/univar_zinnen'
hww_dir = '/media/lukas/data/DecodingEmotions/univar_hww'

zinnen_stats = sorted(glob(op.join(zinnen_dir, '?ope?.*', 'stats', 'zstat?.nii.gz')))
hww_stats = sorted(glob(op.join(hww_dir, '?ope?.*', 'stats', 'zstat?.nii.gz')))

if not op.isdir(conj_dir):
    os.makedirs(conj_dir)

for z, h in zip(zinnen_stats, hww_stats):
    cope = op.basename(op.dirname(op.dirname(z))).split('.')[0]
    zstat = op.basename(z).split('.')[0]
    mask = op.join(op.dirname(op.dirname(z)), 'mask.nii.gz')
    bg = op.join(op.dirname(op.dirname(z)), 'example_func.nii.gz')

    outdir = op.join(conj_dir, cope)
    if not op.isdir(outdir):
        os.makedirs(outdir)

    outname = zstat + '_conj'

    os.chdir(outdir)
    cmd = 'bash %s %s %s %s %f %f %s %s' % (conj_script, z, h, mask,
                                            zmin, pclust, bg, outname)

    os.system(cmd)
