[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8357494.svg)](https://doi.org/10.5281/zenodo.8357494)

## Manifest
- `espaloma-0.3.0rc1-pavan`: Minimize QM structures with `openff-2.0.0` and `espaloma-0.3.0rc1` (former release candidate of espaloma-0.3)  
- `espaloma-0.3.0rc6`: Minimize QM structures with `espaloma-0.3`  
- `openff-2.1.0`: Minimize QM structures with `openff-2.1.0`  
- `compare-models-manuscript`: Stores scripts to compare and analyze QM and MM minimized structures


## Basic Usage
***NOTE:  Steps 1 & 2 could take a while to process. Prefiltered QM datasets and MM optimized structures can be downloaded from [Zenodo](https://doi.org/10.5281/zenodo.8357494).***

1. (Optional) Download QM dataset from QCArchive

    Run the `01a-download.py` script to retrieve the relevant QC data from the QCArchive as a json file (`industry-benchmark-set-result-collection-downloaded.json`). Subsequently, run `01-setup.py` script to filter out and incomplete or undesirable (e.g. records whereby the molecule connectivity changed during the QM minimization) records.
    The processed molecules tagged with information from the QC record, including the CMILES and QC energy, will be stored in a new `01-processed-qm.sdf` file and additionally information about the included records will be stored in `01-processed-qm.json`.

    > cd espaloma-0.3.0rc1-pavan  
    > python 01a-download.py "OpenFF Full Optimization Benchmark 1 v1.1"  
    > python 01-setup.py

2. (Optional) Split sdf file into smaller chunks

    Run the `02-a-chunk-qm.py` script to split the `01-processed-qm.sdf` file produced by STEP 1 into
    many smaller chunks. This allows the next step to be parallelized across many different CPUs / workers.
    By default the split chuncks will be stored in a new `02-chunks/` directory.

    > python 02-a-chunk-qm.py  

    ***NOTE: `02-chunks/` can be downloaded from [Zenodo](https://doi.org/10.5281/zenodo.8357494).***

3. Minimize QM structure with each force field of interest

    The minimized structures using `openff-2.0.0` and `espaloma-0.3.0rc1` was kindly provided by Pavan Behara, by running `02-b-minimize.py`. These minimized structures can be downloaded from [Zenodo](https://doi.org/10.5281/zenodo.8357494) (02-outputs-openff-2.0.0-espaloma-0.3.0rc1.tar.gz).

    To run minimization with `openff-2.1.0`, move to a different directory and run the lsf job script. The minimized structures will be stored in a new `02-outputs/` directory. Similarly, to minimize with `espaloma-0.3`, move to `espaloma-0.3.0rc6/` directory and run the lsf job script.

    > cd openff-2.1.0  
    > bsub < lsf-submit-step02b.sh

    ***NOTE: All MM minimized structures (`02-outputs/`) can be downloaded from [Zenodo](https://doi.org/10.5281/zenodo.8357494).***

4. Compute metric

    Run the `03-a-compute-metric.py` to compute the RMSD, TF, and ddE metrics for each MM force fields. Make sure the path to QM and MM minimized structures are defined correctly in `03-force-fields.json`. Multiple csv files will be exported in `03-outputs/`. 

    > cd compare-models-manuscript  
    > bsub < lsf-submit-step03a.sh

    Run `03-b-join-metrics.py` to concatenate the csv files in `03-outputs/` into a single file (`03-metric.csv`)
    
    > bsub < lsf-submit-step03b.sh


5. Analyze

    Run `analyze.ipynb` to generate cumulative distribution function (CDF) plots of RMSD, TFD, and ddE. To analyze the QM and MM deviation for each valence terms, run `04-plot-metrics.py`. Figures will be exported in `04-outputs/`.

    More detailed analysis can be conducted using `analyze-full.ipynb` and `04-plot-metrics-full.py`.



## Reference
https://github.com/openforcefield/openff-sage/tree/main/inputs-and-results/benchmarks/qc-opt-geo