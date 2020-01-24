# This code will build a new model into the ~/models directory
# To use this new model, change and save the CHURN_MODEL_NAME environment 
# variable


os.environ['DATASET'] = 'wine'
os.environ['MODEL_TYPE'] = 'gb'

from explainer import train
train.train_and_explain_and_save()

#os.environ['MODEL_NAME'] = 'xxxxxxxxxxxx'