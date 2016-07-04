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
# from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from joblib import Parallel, delayed
from skbold.utils import (MvpResults, MvpAverageResults, DataHandler)
from skbold.transformers import *

# Turn-off UserWarning to avoid clutter
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

""" START OF ANALYSIS """

#  Definition of data-dirs
project_dir = '/media/lukas/data/DecodingEmotions/DATA/DATA_MVPA/Optimization_set'
self_dir = op.join(project_dir, 'glm_SELF')
other_dir = op.join(project_dir, 'glm_OTHER')
self_paths = glob.glob(op.join(self_dir, 'sub*'))
other_paths = glob.glob(op.join(other_dir, 'sub*'))

# Analysis parameters
iterations = 100000
n_test = 4
zvalue = 2.3
score_method = 'voting'
resultsdir = 'Optimization_100000'
n_cores = -1

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
                       score_method, pipeline, cutoff, resultsdir):

    self_dir = os.path.dirname(self_path)
    other_dir = os.path.dirname(other_path)

    sub_name = os.path.basename(self_path)
    print('\nProcessing %s' % sub_name)

    # Loading
    self_data = DataHandler(identifier='merged', shape='2D').load_separate_sub(self_path, remove_zeros=False)
    other_data = DataHandler(identifier='', shape='2D').load_separate_sub(other_path, remove_zeros=False)

    # Set params in pipeline
    folds_self = StratifiedShuffleSplit(self_data.y, n_iter=iterations,
                                        test_size=n_test * self_data.n_class)
    folds_other = StratifiedShuffleSplit(other_data.y, n_iter=iterations,
                                         test_size=n_test * self_data.n_class)

    # Results-object initialization
    results_self = MvpResults(self_data, iterations, resultsdir, method=score_method, feature_scoring='coefovo')
    results_other = MvpResults(other_data, iterations, resultsdir, method=score_method, feature_scoring='coefovo')

    # Loop over folds
    for j, folds in enumerate(zip(folds_self, folds_other)):

        if (j+1) % (iterations / 100) == 0:
            print('Iteration: %i' % (j+1))

        f_self, f_other = folds
        s_train_idx, s_test_idx = f_self
        o_train_idx, o_test_idx = f_other

        s_X_train, s_X_test = self_data.X[s_train_idx, :], self_data.X[s_test_idx, :]
        s_y_train, s_y_test = self_data.y[s_train_idx], self_data.y[s_test_idx]

        o_X_train, o_X_test = other_data.X[o_train_idx, :], other_data.X[o_test_idx]
        o_y_train, o_y_test = other_data.y[o_train_idx], other_data.y[o_test_idx]
        pipeline.fit(s_X_train, s_y_train)
        y_pred_s = pipeline.predict_proba(s_X_test)
        results_self.update_results(test_idx=s_test_idx, y_pred=y_pred_s, pipeline=pipeline)

        y_pred_o = pipeline.predict_proba(o_X_test)
        results_other.update_results(test_idx=o_test_idx, y_pred=y_pred_o, pipeline=pipeline)

    # Compute average performance and write results (.csv)
    results_self.compute_score().write_results(self_dir, convert2mni=True)
    results_other.compute_score().write_results(other_dir, convert2mni=True)

Parallel(n_jobs=n_cores)(delayed(run_classification)(self_path, other_path, n_test, iterations, score_method, pipeline,
                                               zvalue, resultsdir) for self_path, other_path in zip(self_paths, other_paths))

# Initialize 'averager' and write results
averager_s = MvpAverageResults(op.join(self_dir, resultsdir), cleanup=False)
averager_o = MvpAverageResults(op.join(other_dir, resultsdir), cleanup=False)
averager_s.average()
averager_o.average()

print('Analysis finished.')
