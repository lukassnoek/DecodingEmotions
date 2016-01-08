"""
Transforms glm estimates to mvpa objects
"""

import os
import shutil
import sys
import numpy as np
import glob
from os.path import join as opj
sys.path.append('/home/lukas/Dropbox/PhD_projects/scikit_BOLD/')
from data2mvpa import glm2mvpa, load_mvp_object
import matplotlib.pyplot as plt

mask = '/home/lukas/Dropbox/PhD_projects/DynamicAffect_Multiscale/ROIs/GrayMatter.nii.gz'

self_dirs = glob.glob('/home/lukas/DecodingEmotions/Self/*/*.feat')
_ = [shutil.rmtree(d) for d in [os.path.dirname(tdir) + '/mvp_data' for tdir in self_dirs] if os.path.exists(d)]
_ = [glm2mvpa(self_dir, mask=mask, beta2tstat=True) for self_dir in self_dirs]

other_dirs = glob.glob('/home/lukas/DecodingEmotions/Other/*/*.feat')
_ = [shutil.rmtree(d) for d in [os.path.dirname(tdir) + '/mvp_data' for tdir in other_dirs] if os.path.exists(d)]
_ = [glm2mvpa(other_dir, remove_class=['cue'], mask=mask, beta2tstat=True) for other_dir in other_dirs]