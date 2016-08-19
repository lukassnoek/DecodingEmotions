import os.path as op
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import StratifiedKFold
from skbold.utils import MvpResultsClassification
from skbold.transformers import MeanEuclidean
from sklearn.svm import SVC

base_dir = '/media/lukas/data/SharedStates/RESULTS/MVPA/Validation/Condition_average_mvpa'
### ARGUMENTS ###

n_folds = 10
out_path = op.join(out_dir, 'self') # change 'self' to e.g. 'other' to do within other-decoding
clf = SVC(kernel='linear', C=1, class_weight='balanced')

mvp = joblib.load(op.join(base_dir, 'mvp_self.jl'))

pipe = Pipeline([('scaler', StandardScaler()),
                 ('ufs', MeanEuclidean(cutoff=2.3)),
                 ('svm', clf)])

mvp_results = MvpResultsClassification(mvp, n_folds, out_path=out_path,
                                       feature_scoring='coef', verbose=True)

folds = StratifiedKFold(mvp.y, n_folds=n_folds)

for train_idx, test_idx in folds:
    train, test = mvp.X[train_idx, :], mvp.X[test_idx, :]
    y_train, y_test = mvp.y[train_idx], mvp.y[test_idx]
    pipe.fit(train, y_train)
    pred = pipe.predict(test)
    mvp_results.update(test_idx, pred, pipeline=pipe)

mvp_results.compute_scores()
mvp_results.write()
mvp_results.save_model(pipe)
