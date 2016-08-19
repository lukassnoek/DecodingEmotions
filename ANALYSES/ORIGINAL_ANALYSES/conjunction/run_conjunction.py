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

base_dir = '/media/lukas/data/SharedStates'
conj_dir = op.join(base_dir, 'RESULTS', 'UNIVARIATE', 'Conjunction_SELF_OTHER')
conj_script = op.join(base_dir, 'ANALYSES', 'ORIGINAL_ANALYSES', 'conjunction', 'easythresh_conj.sh')

self_dir = op.join(base_dir, 'RESULTS', 'UNIVARIATE', 'Grouplevel_SELF')
other_dir = op.join(base_dir, 'RESULTS', 'UNIVARIATE', 'Grouplevel_OTHER')

self_stats = sorted(glob(op.join(self_dir, '?ope?.*', 'stats', 'zstat?.nii.gz')))
other_stats = sorted(glob(op.join(other_dir, '?ope?.*', 'stats', 'zstat?.nii.gz')))

if not op.isdir(conj_dir):
    os.makedirs(conj_dir)

for s, o in zip(self_stats, other_stats):
    cope = op.basename(op.dirname(op.dirname(s))).split('.')[0]
    zstat = op.basename(s).split('.')[0]
    mask = op.join(op.dirname(op.dirname(s)), 'mask.nii.gz')
    bg = op.join(op.dirname(op.dirname(s)), 'example_func.nii.gz')

    outdir = op.join(conj_dir, cope)
    if not op.isdir(outdir):
        os.makedirs(outdir)

    outname = zstat + '_conj'

    os.chdir(outdir)
    cmd = 'bash %s %s %s %s %f %f %s %s' % (conj_script, s, o, mask,
                                            zmin, pclust, bg, outname)

    os.system(cmd)
