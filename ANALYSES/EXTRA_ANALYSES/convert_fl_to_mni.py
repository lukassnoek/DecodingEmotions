import os.path as op
from glob import glob
from skbold.core import convert2mni
from joblib import Parallel, delayed

firstlevel_dir = '/media/lukas/data/SharedStates/RESULTS/UNIVARIATE/Firstlevel*'

stat_dirs = sorted(glob(op.join(firstlevel_dir, '*', 'sub*', 'sub*.feat',
                                'stats')))

def run_parallel(stat):
    print(stat)
    reg_dir = op.join(op.dirname(stat), 'reg')
    fls = glob(op.join(stat, '*.nii.gz'))

    convert2mni(fls, reg_dir, op.join(op.dirname(stat), 'reg_standard'),
                suffix=None)

Parallel(n_jobs=-2)(
    delayed(run_parallel)(stat) for stat in stat_dirs)
