"""
Main analysis script for the Decoding Emotions study.
"""

from __future__ import print_function, division, absolute_import
import glob
import os
import os.path as op
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import StratifiedKFold, StratifiedShuffleSplit
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from joblib import Parallel, delayed, load
from skbold.utils import MvpResultsClassification
from skbold.transformers import *

project_dir = '/media/lukas/data/DecodingEmotions/DATA/DATA_MVPA/Validation_set'
self_dir = op.join(project_dir, 'glm_SELF')
other_dir = op.join(project_dir, 'glm_OTHER')
self_paths = sorted(glob.glob(op.join(self_dir, 'sub*', 'mvp.jl')))
other_paths = sorted(glob.glob(op.join(other_dir, 'sub*', 'mvp.jl')))

# Analysis parameters
iterations = 1000
n_test = 4
zvalue = 2.3
n_cores = 1

# Processing-pipeline
scaler = StandardScaler()
transformer = MeanEuclidean(cutoff=zvalue, normalize=True)
clf = SVC(kernel='linear', probability=True)
pipeline = Pipeline([('transformer', transformer),
                     ('scaler', scaler),
                     ('classifier', clf)])

def run_classification(self_path, other_path, n_test, iterations, pipeline):

    sub_name = os.path.basename(self_path)
    print('\nProcessing %s' % sub_name)

    # Loading
    self_data = load(self_path)
    other_data = load(other_path)

    # Set params in pipeline
    folds_self = StratifiedShuffleSplit(self_data.y, n_iter=iterations,
                                        test_size=3*n_test)
    folds_other = StratifiedShuffleSplit(other_data.y, n_iter=iterations,
                                         test_size=3*n_test)

    # Results-object initialization
    results_self = MvpResultsClassification(self_data, iterations, feature_scoring='coef',
                                            verbose=False)
    results_other = MvpResultsClassification(other_data, iterations, feature_scoring='coef',
                                             verbose=False)

    # Loop over folds
    for j, folds in enumerate(zip(folds_self, folds_other)):

        f_self, f_other = folds
        s_train_idx, s_test_idx = f_self
        o_train_idx, o_test_idx = f_other

        s_X_train, s_X_test = self_data.X[s_train_idx, :], self_data.X[s_test_idx, :]
        s_y_train, s_y_test = self_data.y[s_train_idx], self_data.y[s_test_idx]

        o_X_train, o_X_test = other_data.X[o_train_idx, :], other_data.X[o_test_idx]
        o_y_train, o_y_test = other_data.y[o_train_idx], other_data.y[o_test_idx]

        pipeline.fit(s_X_train, s_y_train)
        y_pred_s = pipeline.predict(s_X_test)
        #results_self.update(test_idx=s_test_idx, y_pred=y_pred_s, values=None)

        y_pred_o = pipeline.predict(o_X_test)
        results_other.update(test_idx=o_test_idx, y_pred=y_pred_o, values=None)

    # Compute average performance and write results (.csv)
    #results_self.compute_scores()
    results_other.compute_scores()

Parallel(n_jobs=n_cores)(delayed(run_classification)(self_path, other_path, n_test, iterations, pipeline)
                         for self_path, other_path in zip(self_paths, other_paths))