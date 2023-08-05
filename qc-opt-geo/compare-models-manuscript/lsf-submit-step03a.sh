#!/bin/bash
#BSUB -J qc-opt-geo
#BSUB -J "array[1-250]"
#BSUB -q cpuqueue
#BSUB -W 8:00
#BSUB -n 1
#BSUB -R rusage[mem=8]
#BSUB -R span[hosts=1]
#BSUB -o lsf-out/out-%J.out
#BSUB -e lsf-out/out-%J.err
#BSUB -L /bin/bash

# Load the necessary modules
source ~/.bashrc

mkdir -p lsf-out
mkdir -p 03-outputs

# Execute the Python scripts
conda activate qc-opt-geo
python 03-a-compute-metrics.py --input "03-force-fields.json" --index "$LSB_JOBINDEX" --output 03-outputs/03-metrics-"$LSB_JOBINDEX".csv
