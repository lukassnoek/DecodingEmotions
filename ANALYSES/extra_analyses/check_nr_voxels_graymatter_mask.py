import os.path as op
import nibabel as nib
import numpy as np
from glob import glob

base_dir = '/media/lukas/data/DecodingEmotions/DATA/DATA_MVPA/Validation_set/glm_OTHER'
gm_masks = glob(op.join(base_dir, 'sub*', '*.feat', 'reg', 'GrayMatter_epi.nii.gz'))
nvox = np.array([(nib.load(m).get_data() > 0).sum() for m in gm_masks])

print("Mean (std) voxels in gray-matter mask in native space: %.3f (%.3f) " %
      (nvox.mean(), nvox.std()))
