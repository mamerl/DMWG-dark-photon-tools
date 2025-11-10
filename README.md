# DMWG Code Instructions

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

## Overview

This repository provides comprehensive documentation, setup instructions, and configuration files for Dark Matter Working Group (DMWG) tools and related software used for reinterpretation of LHC collider searches and dark matter phenomenology studies.

**Target Audience**: High energy physics researchers, phenomenologists, and experimentalists working on dark matter searches and BSM (Beyond the Standard Model) physics interpretations.

## Repository Structure

```
DMWG-code-instructions/
├── MadDM/              # MadDM setup and usage instructions
├── DMWG_codes/         # DMWG-specific tools and code
├── More_tools/         # Additional HEP tools for reinterpretations
├── CITATION.cff        # Citation information
├── CONTRIBUTING.md     # Contribution guidelines
├── CODE_OF_CONDUCT.md  # Code of conduct
├── LICENSE             # GNU GPL v3 license
└── README.md           # This file
```

## Getting Started

### Prerequisites

- Unix-like operating system (Linux, macOS)
- Python 3.7 or higher
- GCC/Gfortran compiler suite
- Git version control

### Quick Start

1. Clone this repository:
```bash
git clone https://github.com/mamerl/DMWG-code-instructions.git
cd DMWG-code-instructions
```

2. Browse the specific tool directory for detailed instructions:
   - [MadDM](./MadDM/README.md) - For dark matter calculations
   - [DMWG_codes](./DMWG_codes/README.md) - For DMWG-specific tools
   - [More_tools](./More_tools/README.md) - For additional analysis tools

## Key Features

- **Comprehensive Documentation**: Step-by-step setup guides for multiple HEP tools
- **FAIR Compliant**: Follows Findability, Accessibility, Interoperability, and Reusability principles
- **Reinterpretation Focus**: Tailored for LHC search reinterpretations
- **Community-Driven**: Open for contributions from the HEP community

## FAIR Principles Compliance

### Findability
- **F1**: Persistent identifier via Zenodo DOI (see badge above)
- **F2**: Rich metadata in `codemeta.json` and `CITATION.cff`
- **F3**: Identifier clearly referenced in metadata
- **F4**: Registered in searchable resources (GitHub, Zenodo)

### Accessibility
- **A1**: Open access via GitHub with public repository
- **A2**: Metadata remains accessible even if data unavailable
- **A3**: Clear authentication and authorization (public read, contributor write)

### Interoperability
- **I1**: Machine-readable metadata formats (JSON, CFF)
- **I2**: Standard vocabularies for HEP (arXiv, inspire-HEP)
- **I3**: Includes references to related resources

### Reusability
- **R1**: Clear GPL-3.0 license
- **R2**: Detailed provenance information
- **R3**: Community standards for HEP software
- **R4**: Usage documentation and examples

## Tools Covered

### Primary Tools
- **MadDM**: Dark matter observables calculator
- **MadGraph5_aMC@NLO**: Matrix element generator
- **MadAnalysis5**: Phenomenological analysis framework

### Supporting Tools
- CheckMATE, SModelS, micrOMEGAs, Delphes, Pythia, Herwig, and more

See [More_tools](./More_tools/README.md) for complete list.

## Use Cases

This repository supports:
- Reinterpretation of ATLAS and CMS searches for dark matter
- Implementation of simplified dark matter models
- Calculation of relic density and detection cross-sections
- Collider phenomenology studies
- Statistical analysis and limit setting

## Citation

If you use resources from this repository in your research, please cite:

```bibtex
@software{dmwg_code_instructions,
  author       = {{DMWG Collaboration}},
  title        = {DMWG Code Instructions},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://github.com/mamerl/DMWG-code-instructions}
}
```

For specific tools, please also cite the original papers (see individual README files).

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- How to report issues
- How to submit pull requests
- Coding standards and guidelines
- Community standards

## Code of Conduct

This project follows a Code of Conduct to ensure a welcoming environment for all contributors. See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

## Support

- **Issues**: [GitHub Issues](https://github.com/mamerl/DMWG-code-instructions/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mamerl/DMWG-code-instructions/discussions)
- **DMWG Resources**: [LHC DM Working Group](https://lpcc.web.cern.ch/content/lhc-dm-wg)

## Related Resources

- [LHC DM Working Group](https://lpcc.web.cern.ch/content/lhc-dm-wg)
- [LHC Reinterpretation Forum](https://twiki.cern.ch/twiki/bin/view/LHCPhysics/InterpretingLHCresults)
- [ATLAS Reinterpretation](https://twiki.cern.ch/twiki/bin/view/AtlasPublic/Reinterpretation)
- [CMS Reinterpretation](https://twiki.cern.ch/twiki/bin/view/CMSPublic/PhysicsResultsSUS)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This work is supported by the LHC Dark Matter Working Group and the broader high energy physics community. We thank all contributors and tool developers whose software is documented here.

---

**Last Updated**: November 2025  
**Maintained by**: DMWG Collaboration  
**Contact**: [Open an issue](https://github.com/mamerl/DMWG-code-instructions/issues)
