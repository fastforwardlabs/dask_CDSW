import os
import importlib


dataset = os.environ.get('DATASET', 'ibm')
load_dataset = (importlib
                .import_module('explainer.data.' + dataset)
                .load_dataset)
