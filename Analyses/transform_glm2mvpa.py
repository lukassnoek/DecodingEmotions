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
from data2mvpa import Fsl2mvp, DataHandler

self_dirs = glob.glob('/home/lukas/DecodingEmotions/Self/*/*.feat')

"""
for dr in self_dirs:
    fsl2mvp = Fsl2mvp(dr, mask=None, mask_threshold=0, remove_class=[],
                 ref_space='epi', beta2tstat=True, cleanup=1)
    fsl2mvp.transform().merge_runs()
"""

mvp_dirs = glob.glob('/home/lukas/DecodingEmotions/Self/*/mvp_data')
test = DataHandler(mvp_dirs[0], identifier='merged', shape='2D').load()