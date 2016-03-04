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
from skbold.utils.mvp_utils import (MvpResults, MvpAverageResults,
                                         DataHandler)
from skbold.transformers.transformers import *

# Turn-off UserWarning to avoid clutter
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

""" START OF ANALYSIS """

#  Definition of data-dirs

def run_classification(self_path, other_path, n_test, iterations,
                       score_method, cutoff):

    scaler = StandardScaler()
    transformer = MeanEuclidean(cutoff=cutoff, normalize=True)
    clf = SVC(kernel='linear', probability=True)
    pipeline = Pipeline([('transformer', transformer),
                     ('scaler', scaler),
                     ('classifier', clf)])

    self_dir = os.path.dirname(self_path)
    other_dir = os.path.dirname(other_path)

    sub_name = os.path.basename(self_path)
    print('\nProcessing %s' % sub_name)

    # Loading
    self_data = DataHandler(identifier='merged', shape='2D').load_separate_sub(self_path)
    other_data = DataHandler(identifier='', shape='2D').load_separate_sub(other_path)

    # Set params in pipeline
    folds_self = StratifiedShuffleSplit(self_data.y, n_iter=iterations,
                                        test_size=n_test * self_data.n_class)
    folds_other = StratifiedShuffleSplit(other_data.y, n_iter=iterations,
                                         test_size=n_test * self_data.n_class)

    # Results-object initialization
    resultsdir = 'results_%f' % cutoff
    results_self = MvpResults(self_data, iterations, resultsdir=resultsdir, method=score_method, feature_scoring='accuracy')
    results_other = MvpResults(other_data, iterations, resultsdir=resultsdir, method=score_method, feature_scoring='accuracy')

    # Loop over folds
    for j, folds in enumerate(zip(folds_self, folds_other)):

        if (j+1) % (iterations / 5) == 0:
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

    return resultsdir
#####

# Analysis parameters
iterations = 5000
n_test = 4
zvalue = np.array([1.5, 1.75, 2., 2.25, 2.5, 2.75])
smooth = ['0mm', '2mm', '5mm', '10mm']
score_method = 'voting'


for sm in smooth:

    project_dir = '/media/lukas/data/DecodingEmotions/Optimization_process/Smoothing_testtrials/%s' % sm
    self_dir = op.join(project_dir, 'glm_zinnen')
    other_dir = op.join(project_dir, 'glm_HWW')
    self_paths = glob.glob(op.join(self_dir, 'sub*'))
    other_paths = glob.glob(op.join(other_dir, 'sub*'))

    for zval in zvalue:
        print('Smoothing: %s, zvalue: %f' % (sm, zval))
        rdir = Parallel(n_jobs=5)(delayed(run_classification)(self_path, other_path, n_test, iterations, score_method,
                                               zval) for self_path, other_path in zip(self_paths, other_paths))

        # Initialize 'averager' and write results
        averager_s = MvpAverageResults(self_dir, rdir[0], cleanup=False)
        averager_o = MvpAverageResults(other_dir, rdir[0], cleanup=False)
        averager_s.average()
        averager_o.average()

print('Analysis finished.')
