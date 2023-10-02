[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8378216.svg)](https://doi.org/10.5281/zenodo.8378216)

# Small molecule geometry benchmark
This repository includes scripts to perform small molecule geometry benchmarks to validate `espaloma-0.3`. 
This repository is part of [espaloma-0.3.0-manuscript](https://github.com/choderalab/espaloma-0.3.0-manuscript).

## Description
Following directories contains the scripts needed to compute the  for a set of force fields against OpenFF Industry Benchmark Season 1 v1.1 dataset, QCArchive optimization data collection.

`espaloma-0.3` (`espaloma-0.3.0rc6`) is quantatively assessed by the measuring the root mean squared deviation (RMSD) in geometries between MM optimized and QM optimized conformers, torsion fingerprint deviation (TFD), and error in relative conformer energies (ddE) against the [OpenFF Industry Benchmark Season 1 v1.1](https://github.com/openforcefield/qca-dataset-submission/tree/master/submissions/2021-06-04-OpenFF-Industry-Benchmark-Season-1-v1.1) deposited in [QCArchive](https://qcarchive.molssi.org/), following the eariler works of the Open Force Field Initiative[1,2].
This dataset is a QM optimization dataset generated at the B3LYP-D3BJ/DZVP level of theory, containing nearly 9847 unique molecules and 76713 conformers of drug-like molecules. RMSD, TFD, ddE metrics are computed for `openff-2.0.0`, `openff-2.1.0`, `gaff-2.11`.

This analysis is based on the [infrastructure](https://github.com/openforcefield/openff-sage/tree/main/inputs-and-results/benchmarks/qc-opt-geo) developed by the Open Force Field Initiative.


## Manifest
- `qc-opt-geo/`: Stores scripts to minimize QM structures various MM force fields  
      - `espaloma-0.3.0rc1-pavan/`  
      - `espaloma-0.3.0rc6/`  
      - `openff-2.1.0/`  
      - `gaff-2.11/`  
      - `compare-models-manuscript/`  
- `envs/`: Stores conda environment file  
      - `environment.yaml`


## Dependencies
Note that [espaloma](https://github.com/choderalab/espaloma) version >=0.3.0 and openeye toolkits are required.


## Citation
If you find this helpful please cite the following:

```
@misc{takaba2023machinelearned,
      title={Machine-learned molecular mechanics force field for the simulation of protein-ligand systems and beyond}, 
      author={Kenichiro Takaba and Iván Pulido and Pavan Kumar Behara and Mike Henry and Hugo MacDermott-Opeskin and John D. Chodera and Yuanqing Wang},
      year={2023},
      eprint={2307.07085},
      archivePrefix={arXiv},
      primaryClass={physics.chem-ph}
}
```

## Reference
[1] [Victoria T. Lim et al. (2020). Benchmark assessment of molecular geometries and energies from small molecule force fields. F1000Research,9:1390](https://f1000research.com/articles/9-1390/v1)
[2] [Simon Boothroyd et al. (2023). Development and Benchmarking of Open Force Field 2.0.0: The Sage Small Molecule Force Field. JCTC,19(11):3251-3275 ](https://pubs.acs.org/doi/10.1021/acs.jctc.3c00039)  
