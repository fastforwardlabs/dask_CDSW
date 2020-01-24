#!/bin/bash

pip3 install -r utils/requirements_s2i.txt

if [ ! -d "model_artifacts" ] 
then
  mkdir model_artifacts
fi

if [ $MODEL_NAME ]
then
  MODEL_FILE="$MODEL_NAME.pkl"

  if [ -f $MODEL_FILE ]
  then 
    mkdir model_artifacts/$MODEL_NAME
    mv $MODEL_FILE model_artifacts/$MODEL_NAME
  fi
fi

if [[ ! -d /home/cdsw/R ]]
then 
  mkdir -m 755 /home/cdsw/R
fi