# More Tools

## Overview

This directory contains additional tools and utilities that complement the main MadDM and DMWG codes for dark matter phenomenology and collider search reinterpretations.

## Included Tools

### Analysis Frameworks

- **MadAnalysis5**: Framework for phenomenological analyses at hadron colliders
- **Rivet**: Robust Independent Validation of Experiment and Theory
- **CheckMATE**: Tool for testing model parameter spaces against LHC constraints
- **SModelS**: Tool for interpreting simplified model results

### Event Generation

- **Pythia**: Event generator for high-energy physics
- **Herwig**: Monte Carlo event generator
- **Delphes**: Fast simulation of particle detector response

### Calculation Tools

- **micrOMEGAs**: Calculation of dark matter relic density and detection rates
- **DarkSUSY**: Dark matter calculations in supersymmetric models
- **MadGraph5_aMC@NLO**: Matrix element generator

### Statistical Tools

- **pyhf**: Pure-Python implementation of HistFactory
- **HEPStats**: Statistical tools for HEP
- **Combine**: CMS statistical analysis tool

## Setup and Installation

Each tool has its own installation requirements. Please refer to the subdirectories for specific instructions.

### General Prerequisites

```bash
# Common dependencies for HEP tools
# Python 3.7+, gcc/gfortran, ROOT (optional), etc.
```

## Quick Reference Links

| Tool | Documentation | Installation | Citation |
|------|--------------|--------------|----------|
| MadAnalysis5 | [Docs](https://madanalysis.irmp.ucl.ac.be/) | [Install](https://madanalysis.irmp.ucl.ac.be/wiki/MA5SandBox) | [arXiv:1206.1599](https://arxiv.org/abs/1206.1599) |
| CheckMATE | [Docs](https://checkmate.hepforge.org/) | [Install](https://checkmate.hepforge.org/download_and_installation) | [arXiv:1611.09856](https://arxiv.org/abs/1611.09856) |
| SModelS | [Docs](https://smodels.github.io/) | [Install](https://smodels.github.io/docs/Installation) | [arXiv:1312.4175](https://arxiv.org/abs/1312.4175) |
| micrOMEGAs | [Docs](https://lapth.cnrs.fr/micromegas/) | [Install](https://lapth.cnrs.fr/micromegas/download.html) | [arXiv:1801.03509](https://arxiv.org/abs/1801.03509) |
| Delphes | [Docs](https://cp3.irmp.ucl.ac.be/projects/delphes) | [Install](https://github.com/delphes/delphes) | [arXiv:1307.6346](https://arxiv.org/abs/1307.6346) |

## Usage Examples

*To be populated with workflow examples combining multiple tools*

### Example Workflow

```bash
# 1. Generate events with MadGraph
# 2. Simulate detector response with Delphes
# 3. Analyze with MadAnalysis5
# 4. Compare with LHC limits using CheckMATE
# 5. Calculate DM observables with micrOMEGAs
```

## Integration Notes

Information on how these tools integrate with MadDM and DMWG codes will be provided here.

## Docker/Singularity Containers

For reproducibility, containerized versions of tools are recommended:

```bash
# Example Docker usage
# docker pull <container-image>
# docker run -it <container-image>
```

## Contributing

Have experience with additional tools? Please contribute! See [CONTRIBUTING.md](../CONTRIBUTING.md).

## Support and Resources

- [HEPForge](https://www.hepforge.org/)
- [CERN Software](https://cern.ch/software)
- [HEP Software Foundation](https://hepsoftwarefoundation.org/)

## License

See [LICENSE](../LICENSE) in the main repository. Individual tools may have their own licenses - please check respective documentation.
