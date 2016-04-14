"""
Main analysis script for the Decoding Emotions study.
"""

from __future__ import print_function, division, absolute_import
import glob
import os
import warnings
import os.path as op
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from joblib import Parallel, delayed
from skbold.utils.mvp_utils import (MvpResults, MvpAverageResults,
                                         DataHandler)
from skbold.transformers.transformers import *

# Turn-off UserWarning to avoid clutter
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

""" START OF ANALYSIS """

#  Definition of data-dirs
project_dir = '/media/lukas/data/DecodingEmotions/Validation_set'
self_dir = op.join(project_dir, 'glm_zinnen')
other_dir = op.join(project_dir, 'glm_HWW')
self_paths = glob.glob(op.join(self_dir, 'sub*'))
other_paths = glob.glob(op.join(other_dir, 'sub*'))

# Analysis parameters
iterations = 10000
n_test = 4
zvalue = 2.3
score_method = 'voting'
resultsdir = 'redo_voxelplots_COEF_ovo'
fs = 'coefovo'
n_cores = 1

# Processing-pipeline
scaler = StandardScaler()
transformer = MeanEuclidean(cutoff=zvalue, normalize=True)
clf = SVC(kernel='linear', probability=True)
pipeline = Pipeline([('transformer', transformer),
                     ('scaler', scaler),
                     ('classifier', clf)])

# Grid-search parameters
# gs_params = dict(euclidean__zvalue=np.linspace(1.5, 2.3, 9))
# pipeline = GridSearchCV(pipeline, param_grid=gs_params, n_jobs=-1)

def run_classification(self_path, other_path, n_test, iterations,
                       score_method, pipeline, cutoff):

    self_dir = os.path.dirname(self_path)

    sub_name = os.path.basename(self_path)
    print('\nProcessing %s' % sub_name)

    # Loading
    self_data = DataHandler(identifier='merged', shape='2D').load_separate_sub(self_path)

    # Set params in pipeline
    folds_self = StratifiedShuffleSplit(self_data.y, n_iter=iterations,
                                        test_size=n_test * self_data.n_class)

    # Results-object initialization
    results_self = MvpResults(self_data, iterations, 'redo_voxelplots_COEF_ovo', method=score_method, feature_scoring=fs)

    # Loop over folds
    for j, fold in enumerate(folds_self):

        if (j+1) % (iterations / 5) == 0:
            print('Iteration: %i' % (j+1))

        s_train_idx, s_test_idx = fold

        s_X_train, s_X_test = self_data.X[s_train_idx, :], self_data.X[s_test_idx, :]
        s_y_train, s_y_test = self_data.y[s_train_idx], self_data.y[s_test_idx]

        pipeline.fit(s_X_train, s_y_train)
        y_pred_s = pipeline.predict_proba(s_X_test)
        results_self.update_results(test_idx=s_test_idx, y_pred=y_pred_s, pipeline=pipeline)

    # Compute average performance and write results (.csv)
    results_self.compute_score().write_results(self_dir, convert2mni=True)

Parallel(n_jobs=n_cores)(delayed(run_classification)(self_path, other_path, n_test, iterations, score_method, pipeline,
                                               zvalue) for self_path, other_path in zip(self_paths, other_paths))

# Initialize 'averager' and write results
averager_s = MvpAverageResults(self_dir, resultsdir, cleanup=False)
averager_s.average()

print('Analysis finished.')
