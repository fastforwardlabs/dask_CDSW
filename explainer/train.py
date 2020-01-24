from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from explainer import utils
from explainer.data import dataset, load_dataset
from explainer.explainedmodel import ExplainedModel
from explainer.models import make_clf

from lime.lime_tabular import LimeTabularExplainer


def count_ohe_features(X, ohe):
    return ohe.fit_transform(X).shape[1]


def train(data, labels):
    ce = utils.CategoricalEncoder()
    X = ce.fit_transform(data)
    y = labels.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    
    categorical_features=list(ce.cat_columns_ix_.values())
    if categorical_features:
      ohe = OneHotEncoder(categorical_features, 
                          sparse=False)
      clf = make_clf(num_features=count_ohe_features(X, ohe))
      pipe = Pipeline([('ohe', ohe), 
                       ('scaler', StandardScaler()), 
                       ('clf', clf)])
    else:
      clf = make_clf()
      pipe = Pipeline([('scaler', StandardScaler()),
                       ('clf', clf)])
    
    pipe.fit(X_train, y_train)
    print("train", pipe.score(X_train, y_train))
    print("test", pipe.score(X_test, y_test))
    print(classification_report(y_test, pipe.predict(X_test)))
    data[labels.name + ' prediction'] = pipe.predict_proba(X)[:, 1]
    #data[labels.name + ' class_pred'] = pipe.predict(X)
    return ce, pipe

def experiment(data, labels):
    ce = utils.CategoricalEncoder()
    X = ce.fit_transform(data)
    y = labels.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    
    categorical_features=list(ce.cat_columns_ix_.values())
    if categorical_features:
      ohe = OneHotEncoder(categorical_features, 
                          sparse=False)
      clf = make_clf(num_features=count_ohe_features(X, ohe))
      pipe = Pipeline([('ohe', ohe), 
                       ('scaler', StandardScaler()), 
                       ('clf', clf)])
    else:
      clf = make_clf()
      pipe = Pipeline([('scaler', StandardScaler()),
                       ('clf', clf)])
    
    pipe.fit(X_train, y_train)
    train_score = pipe.score(X_train, y_train)
    test_score = pipe.score(X_test, y_test)
    print(classification_report(y_test, pipe.predict(X_test)))
    data[labels.name + ' prediction'] = pipe.predict_proba(X)[:, 1]
    return ce, pipe, train_score, test_score
  

def make_explainer(data, labels, ce, pipe):
    # List of length number of features, containing names of features in order
    # in which they appear in X
    feature_names = list(ce.columns_)
    # List of indices of columns of X containing categorical features
    categorical_features = list(ce.cat_columns_ix_.values())
    # List of (index, [cat1, cat2...]) index-strings tuples, where each index
    # is that of a categorical column in X, and the list of strings are the
    # possible values it can take
    categorical_names = {i: ce.classes_[c]
                         for c, i in ce.cat_columns_ix_.items()}
    class_names = ['No ' + labels.name, labels.name]
    explainer = LimeTabularExplainer(ce.transform(data),
                                     feature_names=feature_names,
                                     class_names=class_names,
                                     categorical_features=categorical_features,
                                     categorical_names=categorical_names)
    return explainer


def train_and_explain_and_save():
    data, labels = load_dataset()
    ce, pipe = train(data, labels)
    explainer = make_explainer(data, labels, ce, pipe)
    explainedmodel = ExplainedModel(dataset=dataset, data=data, labels=labels,
                                    categoricalencoder=ce, pipeline=pipe,
                                    explainer=explainer)
    explainedmodel.save()
    return explainedmodel.model_name
  
def experiment_and_save():
    data, labels = load_dataset()
    ce, pipe, train_score, test_score = experiment(data, labels)
    explainer = make_explainer(data, labels, ce, pipe)
    explainedmodel = ExplainedModel(dataset=dataset, data=data, labels=labels,
                                    categoricalencoder=ce, pipeline=pipe,
                                    explainer=explainer)
    explainedmodel.save()
    return train_score, test_score, explainedmodel.model_path

if __name__ == '__main__':
    utils.log_environment()
    print(train_and_explain_and_save())