"""
Main analysis script for the Decoding Emotions study.
"""

import os
import glob
import sys
sys.path.append('/home/lukas/Dropbox/PhD_projects/scikit_BOLD/')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import join as opj

from data2mvpa import load_mvp_object

# Preprocessing / transformers / models
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.svm import SVC
from transformers import AnovaCutoff
from transformers import ClusterThreshold
from sklearn.feature_selection import VarianceThreshold
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline

project_dir = '/home/lukas/DecodingEmotions'
self_dir, other_dir = opj(project_dir, 'Self'), opj(project_dir, 'Other')

self_paths = glob.glob(opj(self_dir, '*', 'mvp_data'))
other_paths = glob.glob(opj(other_dir, '*', 'mvp_data'))

# Parameters
iterations = 2
n_test = 3

s_sub = np.zeros((len(self_paths), 1))
o_sub = np.zeros((len(self_paths), 1))

for i in range(len(self_paths)):

    sub_name = os.path.basename(os.path.dirname(self_paths[i]))
    print("Processing %s" % sub_name)

    # Loading
    self = load_mvp_object(self_paths[i], identifier='merged')
    other = load_mvp_object(other_paths[i], identifier='')

    # Transforming string labels to numeric
    self.y = LabelEncoder().fit_transform(self.class_labels)
    other.y = LabelEncoder().fit_transform(other.class_labels)

    self.X = StandardScaler().fit_transform(self.X)
    other.X = StandardScaler().fit_transform(other.X)

    folds_self = StratifiedShuffleSplit(self.y, n_iter=iterations, test_size=n_test*self.n_class)
    folds_other = StratifiedShuffleSplit(other.y, n_iter=iterations, test_size=n_test*other.n_class)

    scores = np.zeros((iterations, 2))

    gs_params = dict(clustering__cutoff=np.linspace(1, 10, 13),
                     clustering__min_cluster_size=np.linspace(10, 50, 10))

    transformer = ClusterThreshold(self.mask_shape, self.mask_index, 5, 40)
    clf = SVC(kernel='linear')
    pipeline = Pipeline([('clustering', transformer), ('classifier', clf)])
    grid_search = GridSearchCV(pipeline, param_grid=gs_params, n_jobs=-1)

    for j, folds in enumerate(zip(folds_self, folds_other)):

        #if (i+1) % 10 == 0:
        #    print("Iteration: %i" % (i+1))

        f_self, f_other = folds
        self_train_idx, self_test_idx = f_self
        other_train_idx, other_test_idx = f_other

        s_X_train, s_X_test = self.X[self_train_idx, :], self.X[self_test_idx]
        s_y_train, s_y_test = self.y[self_train_idx], self.y[self_test_idx]

        o_X_train, o_X_test = other.X[other_train_idx, :], other.X[other_test_idx]
        o_y_train, o_y_test = other.y[other_train_idx], other.y[other_test_idx]

        grid_search.fit(s_X_train, s_y_train)
        #transformer.fit(s_X_train, s_y_train)
        #s_X_train = transformer.transform(s_X_train)
        #s_X_test = transformer.transform(s_X_test)
        #o_X_test = transformer.transform(o_X_test)

        #clf.fit(s_X_train, s_y_train)
        grid_search.score(s_X_test, s_y_test)
        #scores[j, 0] = clf.score(s_X_test, s_y_test)
        #scores[j, 1] = clf.score(o_X_test, o_y_test)

    s_sub[i] = scores[:, 0].mean()
    o_sub[i] = scores[:, 1].mean()

    print("Score self: %f \nScore other: %f" % (s_sub[i], o_sub[i]))

s_final = s_sub.mean()
o_final = o_sub.mean()

print("Final score self: %f \nFinal score other: %f" % (s_final, o_final))

