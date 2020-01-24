import os
import sys
from collections import ChainMap
from pandas.io.json import dumps as jsonify

sys.path.append("/home/cdsw") 

from explainer.utils import log_environment
from explainer.explainedmodel import ExplainedModel


#os.environ['MODEL_NAME'] = '20200119T234034_wine_gb'
em = ExplainedModel(os.getenv('MODEL_NAME', 'test_model'))

def predict(args):
    data = dict(ChainMap(args, em.default_data))
    data = em.cast_dct(data)
    probability, class_pred, explanation = em.explain_dct_class(data)
    return jsonify({'quality_prediction': class_pred})
  
def explain(args):
    data = dict(ChainMap(args, em.default_data))
    data = em.cast_dct(data)
    probability, class_pred, explanation = em.explain_dct_class(data)
    return jsonify({'data': dict(data),
                    'quality_prediction': class_pred,
                    'explanation': explanation})
  

#test
#Poor_args={"fixedAcidity":7.4, "volatileAcidity":0.7, "citricAcid":0, "residualSugar":1.9, "chlorides":0.076,  "freeSulfurDioxide":11, "totalSulfurDioxide":34, "density":0.9978, "pH":3.51, "sulphates":0.56, "Alcohol":9.4}
#Excellent_args={"fixedAcidity":5.9, "volatileAcidity":0.550, "citricAcid":0.10, "residualSugar":2.2, "chlorides":0.062,  "freeSulfurDioxide":39.0, "totalSulfurDioxide":51.0, "density":0.99512, "pH":3.52, "sulphates":0.76, "Alcohol":11.2}
#predict(Poor_args)
#predict(Excellent_args)
#explain(Poor_args)
#explain(Excellent_args)