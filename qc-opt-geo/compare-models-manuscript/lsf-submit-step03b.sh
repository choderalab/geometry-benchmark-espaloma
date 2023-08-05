#!/bin/bash
#BSUB -J qc-opt-geo
#BSUB -q cpuqueue
#BSUB -W 04:00
#BSUB -n 1
#BSUB -R rusage[mem=8]
#BSUB -R span[hosts=1]
#BSUB -o out-%J.out
#BSUB -e out-%J.err
#BSUB -L /bin/bash

# Load the necessary modules
source ~/.bashrc

# Execute the Python scripts
conda activate qc-opt-geo
python 03-b-join-metrics.py 03-outputs/* -o 03-metrics.csv
