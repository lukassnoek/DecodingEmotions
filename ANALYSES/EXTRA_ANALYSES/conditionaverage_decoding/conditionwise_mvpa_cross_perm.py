import os.path as op
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import StratifiedKFold
from skbold.utils import MvpResultsClassification
from skbold.transformers import MeanEuclidean, ArrayPermuter
from sklearn.svm import SVC

base_dir = '/media/lukas/data/SharedStates/RESULTS/MVPA/Validation/Condition_average_mvpa'
### ARGUMENTS ###

n_iter = 1000
n_folds = 10
clf = SVC(kernel='linear', C=1, class_weight='balanced')

mvp = joblib.load(op.join(base_dir, 'mvp_other.jl'))
mvp_cross = joblib.load(op.join(base_dir, 'mvp_self.jl'))

pipe = Pipeline([('scaler', StandardScaler()),
                 ('ufs', MeanEuclidean(cutoff=2.3)),
                 ('perm', ArrayPermuter()),
                 ('svm', clf)])

for i in range(n_iter):
    print('iter %i' % (i+1))
    out_path = op.join(base_dir, 'other>>self',
                       'perm_%i' % (i+1))
    mvp_results = MvpResultsClassification(mvp_cross, n_folds,
                                           out_path=out_path,
                                           feature_scoring='fwm', verbose=False)

    folds = StratifiedKFold(mvp.y, n_folds=n_folds, shuffle=True)

    for train_idx, test_idx in folds:
        train, test = mvp.X[train_idx, :], mvp.X[test_idx, :]
        y_train, y_test = mvp.y[train_idx], mvp.y[test_idx]
        pipe.fit(train, y_train)
        pred = pipe.predict(ArrayPermuter().fit_transform(mvp_cross.X))
        mvp_results.update(range(mvp_cross.y.size), pred, pipeline=pipe)

    mvp_results.compute_scores()
    print(mvp_results.confmat)
    mvp_results.write(feature_viz=True, confmat=True, to_tstat=True)
