import glob
import os
from scikit_bold.data2mvp.glm2mvp import Fsl2mvp

mask = '/media/lukas/data/DecodingEmotions/GrayMatter.nii.gz'
mask_threshold = 0

opt_dirs_hww = glob.glob('/media/lukas/data/DecodingEmotions/Optimization_set/glm_HWW/*/*.feat')

for d in opt_dirs_hww:
	converter = Fsl2mvp(d, mask_threshold=mask_threshold, beta2tstat=True, ref_space='epi', mask_path=mask,
				   remove_class=['Cue'])
	converter.glm2mvp()

opt_dirs_zinnen = glob.glob('/media/lukas/data/DecodingEmotions/Optimization_set/glm_zinnen/*/*.feat')


for d in opt_dirs_zinnen:
	converter = Fsl2mvp(d, mask_threshold=mask_threshold, beta2tstat=True, ref_space='epi', mask_path=mask,
				   remove_class=[])
	converter.glm2mvp().merge_runs()

val_dirs_hww = glob.glob('/media/lukas/data/DecodingEmotions/Validation_set/glm_HWW/*/*.feat')
for d in val_dirs_hww:
	converter = Fsl2mvp(d, mask_threshold=mask_threshold, beta2tstat=True, ref_space='epi', mask_path=mask,
				   remove_class=['Cue'])
	converter.glm2mvp()

val_dirs_zinnen = glob.glob('/media/lukas/data/DecodingEmotions/Validation_set/glm_zinnen/*/*.feat')
for d in val_dirs_zinnen:
	converter = Fsl2mvp(d, mask_threshold=mask_threshold, beta2tstat=True, ref_space='epi', mask_path=mask,
				   remove_class=[])
	converter.glm2mvp().merge_runs()
