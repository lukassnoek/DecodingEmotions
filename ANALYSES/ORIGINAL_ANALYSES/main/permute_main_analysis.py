"""
Permutation of main analysis for the SharedStates study.
"""

from __future__ import print_function, division, absolute_import
import glob
import os
import sys
import warnings
import os.path as op
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.svm import SVC
# from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from scikit_bold.utils.mvp_utils import (MvpResults, DataHandler)
from scikit_bold.transformers.transformers import *

# Turn-off UserWarning to avoid clutter
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

""" START OF ANALYSIS """

#  Definition of data-dirs
project_dir = '/media/lukas/data/SharedStates/DATA/MVPA/Validation'
self_dir = op.join(project_dir, 'glm_SELF')
other_dir = op.join(project_dir, 'glm_OTHER')
self_paths = glob.glob(op.join(self_dir, 'sub*'))
other_paths = glob.glob(op.join(other_dir, 'sub*'))

# Analysis parameters
iterations = 1000
n_test = 4
zvalue = 2.3
score_method = 'voting'

# Processing-pipeline
scaler = StandardScaler()
transformer = MeanEuclidean(cutoff=zvalue, normalize=True)
permuter = ArrayPermuter()
clf = SVC(kernel='linear', probability=True)
pipeline = Pipeline([('transformer', transformer),
                     ('scaler', scaler),
                     ('permuter', permuter),
                     ('classifier', clf)])

# Grid-search parameters
# gs_params = dict(euclidean__zvalue=np.linspace(1.5, 2.3, 9))
# pipeline = GridSearchCV(pipeline, param_grid=gs_params, n_jobs=-1)

perm_nr = sys.argv[1]
print('Permutation: %s' % perm_nr)

def run_classification(self_path, other_path, n_test, iterations,
                       score_method, pipeline, cutoff, perm_nr):

    self_dir = os.path.dirname(self_path)
    other_dir = os.path.dirname(other_path)

    # Loading
    self_data = DataHandler(identifier='merged', shape='2D').load_separate_sub(self_path, remove_zeros=False)
    other_data = DataHandler(identifier='', shape='2D').load_separate_sub(other_path, remove_zeros=False)

    # Set params in pipeline
    folds_self = StratifiedShuffleSplit(self_data.y, n_iter=iterations,
                                        test_size=n_test * self_data.n_class)
    folds_other = StratifiedShuffleSplit(other_data.y, n_iter=iterations,
                                         test_size=n_test * self_data.n_class)

    # Results-object initialization
    results_self = MvpResults(self_data, iterations, method=score_method, feature_scoring='coefovo')
    results_other = MvpResults(other_data, iterations, method=score_method, feature_scoring='coefovo')

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
        y_pred_s = pipeline.predict_proba(s_X_test)
        results_self.update_results(test_idx=s_test_idx, y_pred=y_pred_s, pipeline=pipeline)

        y_pred_o = pipeline.predict_proba(o_X_test)
        results_other.update_results(test_idx=o_test_idx, y_pred=y_pred_o, pipeline=pipeline)

    # Compute average performance and write results (.csv)
    results_self.compute_score().write_results_permutation(self_dir, perm_nr)
    results_other.compute_score().write_results_permutation(other_dir, perm_nr)

Parallel(n_jobs=10)(delayed(run_classification)(self_path, other_path, n_test, iterations, score_method, pipeline,
                                               zvalue, perm_nr) for self_path, other_path in zip(self_paths, other_paths))
