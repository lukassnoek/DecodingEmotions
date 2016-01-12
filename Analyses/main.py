"""
Main analysis script for the Decoding Emotions study.
"""

import os
import glob
import warnings
import sys
sys.path.append('/home/lukas/Dropbox/PhD_projects/scikit_BOLD/')

import numpy as np
from os.path import join as opj
from data2mvpa import DataHandler
from mvp_utils import MvpResults, MvpAverageResults
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.svm import SVC
from transformers import AnovaCutoff, ClusterThreshold, MeanEuclideanTransformer
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline

# Turn-off UserWarning to avoid clutter (occurs in univariate feature selection)
warnings.filterwarnings('ignore', category=UserWarning)

""" START OF ANALYSIS """

#  Definition of data-dirs
project_dir = '/home/lukas/DecodingEmotions'
self_dir, other_dir = opj(project_dir, 'Self'), opj(project_dir, 'Other')

self_paths = glob.glob(opj(self_dir, '*', 'mvp_data'))
other_paths = glob.glob(opj(other_dir, '*', 'mvp_data'))

### Analysis parameters ###
iterations = 30000
n_test = 4

# Processing-pipeline
transformer = MeanEuclideanTransformer(zvalue=3)
clf = SVC(kernel='linear')
pipeline = Pipeline([('zvalue_cutoff', transformer), ('classifier', clf)])

# Grid-search parameters
gs_params = dict(zvalue_cutoff__zvalue=np.linspace(1.5, 2.3, 9))
gs_pipeline = GridSearchCV(pipeline, param_grid=gs_params, n_jobs=-1)
gs = False

### Loop over subjects ###
for i in range(len(self_paths)):

    sub_name = os.path.basename(os.path.dirname(self_paths[i]))
    print('\nProcessing %s' % sub_name)

    # Loading
    self_data = DataHandler(self_paths[i], identifier='merged', shape='2D').load()
    other_data = DataHandler(other_paths[i], identifier='', shape='2D').load()

    # Transforming string labels to numeric
    self_data.y = LabelEncoder().fit_transform(self_data.class_labels)
    other_data.y = LabelEncoder().fit_transform(other_data.class_labels)

    self_data.X = StandardScaler().fit_transform(self_data.X)
    other_data.X = StandardScaler().fit_transform(other_data.X)

    test_size = n_test*self_data.n_class
    folds_self = StratifiedShuffleSplit(self_data.y, n_iter=iterations,
                                        test_size=test_size)
    folds_other = StratifiedShuffleSplit(other_data.y, n_iter=iterations,
                                         test_size=test_size)

    # Results-object initialization
    results_self = MvpResults(self_data, iterations, n_test, method='trial-based')
    results_other = MvpResults(other_data, iterations, n_test, method='trial-based')

    ### Loop over folds ###
    for j, folds in enumerate(zip(folds_self, folds_other)):

        if (j+1) % 100 == 0:
            print('Iteration: %i' % (j+1))

        f_self, f_other = folds
        s_train_idx, s_test_idx = f_self
        o_train_idx, o_test_idx = f_other

        s_X_train, s_X_test = self_data.X[s_train_idx, :], self_data.X[s_test_idx, :]
        s_y_train, s_y_test = self_data.y[s_train_idx], self_data.y[s_test_idx]

        o_X_train, o_X_test = other_data.X[o_train_idx, :], other_data.X[o_test_idx]
        o_y_train, o_y_test = other_data.y[o_train_idx], other_data.y[o_test_idx]

        if gs:
            gs_pipeline.fit(s_X_train, s_y_train)
            y_pred_s = gs_pipeline.predict(s_X_test)
            y_pred_o = gs_pipeline.predict(o_X_test)
        else:
            pipeline.fit(s_X_train, s_y_train)
            y_pred_s = pipeline.predict(s_X_test)
            y_pred_o = pipeline.predict(o_X_test)

        # Compute number of features used in analysis
        n_feat = np.sum(pipeline.named_steps['zvalue_cutoff'].idx_)

        # Update results with current iteration
        results_self.update_results(j, n_feat, s_test_idx, y_pred_s)
        results_other.update_results(j, n_feat, o_test_idx, y_pred_o)

    # Compute average performance and write results (.csv)
    results_self.compute_score().write_results(project_dir)
    results_other.compute_score().write_results(project_dir)

# Initialize 'averager' and write results
averager_s = MvpAverageResults(project_dir, 'Zinnen', write_df=True, cleanup=True)
averager_o = MvpAverageResults(project_dir, 'HWW', write_df=True, cleanup=True)
averager_s.load().write()
averager_o.load().write()

print('Analysis finished.')

""" END OF ANALYSIS """