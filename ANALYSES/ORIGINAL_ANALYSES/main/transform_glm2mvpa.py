import glob
import os
import os.path as op
from skbold.data2mvp import Fsl2mvp
from skbold import roidata_path

base_dir = '/media/lukas/data/SharedStates/DATA/MVPA'
mask = os.path.join(roidata_path, 'GrayMatter.nii.gz')
mask_threshold = 0

opt_dirs_hww = glob.glob(op.join(base_dir, 'Optimization/glm_OTHER/*/*.feat'))

for d in opt_dirs_hww:
	converter = Fsl2mvp(d, mask_threshold=mask_threshold, beta2tstat=True, ref_space='epi', mask_path=mask,
				   remove_class=['Cue'])
	converter.glm2mvp()

opt_dirs_zinnen = glob.glob(op.join(base_dir, 'Optimization/glm_SELF/*/*.feat'))

for d in opt_dirs_zinnen:
	converter = Fsl2mvp(d, mask_threshold=mask_threshold, beta2tstat=True, ref_space='epi', mask_path=mask,
				   remove_class=[])
	converter.glm2mvp().merge_runs()

val_dirs_hww = glob.glob(op.join(base_dir, 'Validation/glm_OTHER/*/*.feat'))

for d in val_dirs_hww:
	converter = Fsl2mvp(d, mask_threshold=mask_threshold, beta2tstat=True, ref_space='epi', mask_path=mask,
				   remove_class=['Cue'])
	converter.glm2mvp()

val_dirs_zinnen = glob.glob(op.join(base_dir, 'Validation/glm_SELF/*/*.feat'))
for d in val_dirs_zinnen:
	converter = Fsl2mvp(d, mask_threshold=mask_threshold, beta2tstat=True, ref_space='epi', mask_path=mask,
				   remove_class=[])
	converter.glm2mvp().merge_runs()
