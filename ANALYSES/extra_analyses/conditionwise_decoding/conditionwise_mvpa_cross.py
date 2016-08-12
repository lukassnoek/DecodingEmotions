import os.path as op
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import StratifiedKFold
from skbold.utils import MvpResultsClassification
from skbold.transformers import MeanEuclidean
from sklearn.svm import SVC

base_dir = '/media/lukas/data/DecodingEmotions/RESULTS/MVPA_RESULTS/Validation_set/Condition_average_mvpa'
### ARGUMENTS ###

n_folds = 10
out_path = op.join(base_dir, 'other>>self')
clf = SVC(kernel='linear', C=1, class_weight='balanced')

mvp = joblib.load(op.join(base_dir, 'mvp_other.jl'))
mvp_cross = joblib.load(op.join(base_dir, 'mvp_self.jl'))

pipe = Pipeline([('scaler', StandardScaler()),
                 ('ufs', MeanEuclidean(cutoff=2.3)),
                 ('svm', clf)])

mvp_results = MvpResultsClassification(mvp_cross, n_folds, out_path=out_path,
                                       feature_scoring='coef', verbose=True)

folds = StratifiedKFold(mvp.y, n_folds=n_folds)

for train_idx, test_idx in folds:
    train, test = mvp.X[train_idx, :], mvp.X[test_idx, :]
    y_train, y_test = mvp.y[train_idx], mvp.y[test_idx]
    pipe.fit(train, y_train)
    pred = pipe.predict(mvp_cross.X)
    mvp_results.update(range(mvp_cross.y.size), pred, pipeline=pipe)

mvp_results.compute_scores()
mvp_results.write()
mvp_results.save_model(pipe)