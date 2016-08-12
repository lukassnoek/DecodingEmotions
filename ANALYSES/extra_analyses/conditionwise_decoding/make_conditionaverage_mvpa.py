import os.path as op
from skbold import roidata_path
from skbold.data2mvp import MvpWithin
from glob import glob
from skbold import roidata_path

base_dir = '/media/lukas/data/DecodingEmotions/RESULTS/UNIVARIATE_RESULTS/'
other_dirs = sorted(glob(op.join(base_dir, 'FirstLevel_other', 'sub*', '*.feat')))

mvp = MvpWithin(
    source=other_dirs,
    read_labels=True,
    remove_contrast=['action', 'interoception', 'situation'],
    invert_selection=True,
    ref_space='mni',
    beta2tstat=True,
    remove_zeros=False,
    mask=op.join(roidata_path, 'GrayMatter.nii.gz')
)

mvp.create()
mvp.write(path=base_dir, name='mvp_other')

self_dirs = sorted(glob(op.join(base_dir, 'FirstLevel_self', 'sub*', '*.feat')))

mvp = MvpWithin(
    source=self_dirs,
    read_labels=True,
    remove_contrast=['action', 'interoception', 'situation'],
    invert_selection=True,
    ref_space='mni',
    beta2tstat=True,
    remove_zeros=False,
    mask=op.join(roidata_path, 'GrayMatter.nii.gz')
)

mvp.create()
mvp.write(path=base_dir, name='mvp_self')