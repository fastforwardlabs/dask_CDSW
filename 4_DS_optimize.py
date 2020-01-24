#This code will train a model



from churnexplainer import train
from churnexplainer.data import dataset, load_dataset
import cdsw

#Set model type to one of linear | gb | nonlinear | voting"
#For CML Experiments across multiple model types comment this line out 
#and pass via arguments to the experiment. 
#os.environ['MODEL_TYPE'] = 'gb'
os.gentenv('MODEL_TYPE', sys.argv[1])

# ibm | breastcancer | iris | telco | wine
#os.environ['DATASET'] = 'wine'
os.gentenv('DATASET', sys.argv[2])

train_score, test_score, model_path = train.experiment_and_save()

cdsw.track_metric("train_score",round(train_score,2))
cdsw.track_metric("test_score",round(test_score,2))
cdsw.track_metric("model_path",model_path)
cdsw.track_file(model_path)