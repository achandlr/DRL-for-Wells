#!/bin/bash

source /u/mgiordan/.bashrc

conda activate ml
/u/mgiordan/miniconda3/envs/ml/bin/python train.py $1 $2
