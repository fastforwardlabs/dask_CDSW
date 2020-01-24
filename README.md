# Refractor (for Wine Quality Prediction)

This is the CML port of the Refractor prototype which is part of the [Interpretability
report from Cloudera Fast Forward Labs](https://clients.fastforwardlabs.com/ff06/report).

## CML Applications: Train and inspect a new model locally

This project uses the Applications feature of CML (>=1.2) and CDSW (>=1.7) to instantiate a UI frontend for visual interpretability and decision management.  

### Train a predictor model
A model has been pre-trained and placed in the models directory.  
Start a Python 3 Session with at least 8GB of memory and __run the utils/setup.py code__.  This will create the minimum setup to use existing, pretrained models.  

If you want to retrain the model run the train.py code to train a new model.  

The model artifact will be saved in the models directory named after the datestamp, dataset and algorithm (ie. 20191120T161757_wine_gb). The default settings will create a gradiant boosted classifier model against the wine dataset. However, the code is vary modular and can train multiple model types against essentially any tabular dataset (see below for details).  

### Deploy Predictor and Explainer models
Go to the **Models** section and create a new predictor model.   The sample features below should predict an "Poor" quality wine.
* **Name**: Predictor
* **Description**: Predict wine quality
* **File**: deploy_model.py
* **Function**: predict
* **Input**: 
`{"fixedAcidity":7.4, "volatileAcidity":0.7, "citricAcid":0, "residualSugar":1.9, "chlorides":0.076,  "freeSulfurDioxide":11, "totalSulfurDioxide":34, "density":0.9978, "pH":3.51, "sulphates":0.56, "Alcohol":9.4}`  
* **Kernel**: Python 3

If you created your own model (see above)
* Click on "Set Environment Variables" and add:
  * **Name**: MODEL_NAME
  * **Value**: 20191120T161757_wine_gb  **your model name from above**
  Click "Add" and "Deploy Model"

Create a new Explainer model. The sample features below should predict an "Excellent" quality wine.

* **Name**: Explainer
* **Description**: Explain wine quality prediction
* **File**: deploy_model.py
* **Function**: explain
* **Input**: `{"fixedAcidity":5.9, "volatileAcidity":0.550, "citricAcid":0.10, "residualSugar":2.2, "chlorides":0.062,  "freeSulfurDioxide":39.0, "totalSulfurDioxide":51.0, "density":0.99512, "pH":3.52, "sulphates":0.76, "Alcohol":11.2}`
* **Kernel**: Python 3

If you created your own model (see above)
* Click on "Set Environment Variables" and add:
  * **Name**: MODEL_NAME
  * **Value**: 20191120T161757_wine_gb  **your model name from above**
  Click "Add" and "Deploy Model"

In the deployed Explainer model -> Settings note (copy) the "Access Key" (ie. mukd9sit7tacnfq2phhn3whc4unq1f38)


### Instatiate the flask UI application
From the Project level click on "Open Workbench" (note you don't actually have to Launch a session) in order to edit a file.
Select the flask/single_view.html file and paste the Access Key in at line 19. 
Save and go back to the Project.  

Go to the **Applications** section and select "New Application" with the following:
* **Name**: Visual Wine Analysis
* **Subdomain**: wine-prediction
* **Script**: flask_app.py
* **Kernel**: Python 3
* **Engine Profile**: 1vCPU / 2 GiB Memory  

If you created your own model (see above)
* Add Environment Variables:  
  * **Name**: MODEL_NAME  
  * **Value**: 20191120T161757_wine_gb  **your model name from above**  
  Click "Add" and "Deploy Model"  
  
  
After the Application deploys, click on the blue-arrow next to the name.  The initial view is a table of rows selected at  random from the dataset.  This shows a global view of which features are most important for the prediction made.  

Clicking on any single row will show a "local" interpretabilty of a particular instance.  Here you 
can see how adjusting any one of the features will change the instance's prediction.  

## Additional options
By default this code trains a gradiant boosted classifier for the wine dataset.  
There are other datasets and other model types as well.  Look at run_experiment.py for examples or set the Project environment variables to try other datasets and models:  
Name              Value  
DATASET     ibm (default) | breastcancer | iris  
MODEL_TYPE  linear (default) | gb | nonlinear | voting  


**NOTE** that not all of these options have been fully tested so your mileage may vary.
