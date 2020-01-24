import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

def make_clf(*args, **kwargs):
    clf = RandomForestClassifier(random_state=10, n_jobs=-1)
    param_dist = {"n_estimators": [50, 100, 500, 1000],
                  "max_depth": [5,10,15]}
    return GridSearchCV(clf, param_dist, verbose=10, n_jobs=-2)