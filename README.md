# Small molecule geometry benchmark
This repository includes scripts to perform small molecule geometry benchmarks to validate `espaloma-0.3`. 


## Description
`espaloma-0.3` is quantatively assessed by measuring how well the QM optimized conformer geometries and energies were preserved after minimization. [OpenFF Industry Benchmark Season 1 v1.1](https://github.com/openforcefield/qca-dataset-submission/tree/master/submissions/2021-06-04-OpenFF-Industry-Benchmark-Season-1-v1.1) deposited in [QCArchive](https://qcarchive.molssi.org/), which was generated at B3LYP-D3BJ/DZVP level of theory. This dataset contains nearly 9847 unique molecules and 76713 conformers of drug-like molecules. 
The MM optimized molecules are assessed by measuring the root mean squared deviation (RMSD) in geometries between MM optimized and QM optimized conformers, torsion fingerprint deviation (TFD), and error in relative conformer energies (ddE). `espaloma-0.3` is compared with `openff-2.0.0`, `openff-2.1.0` and `espaloma-0.3-rc1` (a release candidate of `espaloma-0.3`).

This benchmark study heavily relies on the eariler works of the Open Force Field Initiative[1,2] and its [infrastructure](https://github.com/openforcefield/openff-sage/tree/main/inputs-and-results/benchmarks/qc-opt-geo).


## Manifest
- `qc-opt-geo`   
      - `espaloma-0.3.0rc1-pavan`: Minimize QM structures with `openff-2.0.0` and `espaloma-0.3-rc1`  
      - `espaloma-0.3.0rc6`: Minimize QM structures with `espaloma-0.3`  
      - `openff-2.1.0`: Minimize QM structures with `openff-2.1.0`  
      - `compare-models-manuscript`: Stores scripts to compare and analyze QM and MM minimized structures
- `envs/`: Stores conda environment file  
      - `environment.yaml`


## Dependencies
Note that [espaloma](https://github.com/choderalab/espaloma) version 0.3.0 or higher is required.


## Citation
If you find this helpful please cite the following:

```
@misc{takaba2023espaloma030,
      title={Espaloma-0.3.0: Machine-learned molecular mechanics force field for the simulation of protein-ligand systems and beyond}, 
      author={Kenichiro Takaba and Iván Pulido and Mike Henry and Hugo MacDermott-Opeskin and John D. Chodera and Yuanqing Wang},
      year={2023},
      eprint={2307.07085},
      archivePrefix={arXiv},
      primaryClass={physics.chem-ph}
}
```

## Reference
[1] [Simon Boothroyd et al. (2023). Development and Benchmarking of Open Force Field 2.0.0: The Sage Small Molecule Force Field. JCTC,19(11):3251-3275 ](https://pubs.acs.org/doi/10.1021/acs.jctc.3c00039)  
[2] [Victoria T. Lim et al. (2020). Benchmark assessment of molecular geometries and energies from small molecule force fields. F1000Research,9:1390](https://f1000research.com/articles/9-1390/v1)