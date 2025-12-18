# Prototypes of DMWG Run 3 interpretations

This repository contains a collection of code and setup instructions for different packages. The code is heavily based on interpretations for Run 3 ATLAS dijet searches, but it could be adapted for other signatures (e.g. mono-X, etc.).

For steps in the interpretation that rely on re-scaling DMsimp_s_spin1 model limits, the DMWG-couplingScan-code is used. You can use that code to convert your limits into something expected for the dark photon interpretation code (`dark_photon.py`). The `dark_photon.py` script assumes that your input limit corresponds to a model with $g_{\mathrm{DM}} = 1$ and $g_{\ell} = 0$ for a vector Z' mediator.

> Note: the current version of the DMWG-couplingScan-code submodule points to Max Amerl's personal fork of the DMWG project. This will be updated in the future after some changes are added to the central DMWG project.

## Installation and setup

To run the code a basic conda installation is needed. 

> First make sure you have conda installed on your laptop or cluster. If you cannot install conda on a cluster but you have sufficient disk space, miniconda is another option: https://www.anaconda.com/docs/getting-started/miniconda/main.

The environment (packages, etc.) needed are outlined in `environment.yml`, including LHAPDF, which is required by `DMWG-couplingScan-code`. For first time use, run `source install.sh` to setup an environment (it will be called `dmwg-coupling-scan`). For future work just run `source setup.sh` to setup the environment again.

More information on LHAPDF installation is included in the DMWG-couplingScan-code repository in case you prefer another installation procedure.

## Dark photon interpretations
To run these tools you need the json input files discussed in `inputs/README.md`, corresponding to the raw coupling limits (e.g. those provided in HEPData) for a search. Examples are provided based on the ATLAS Run 2 dijet Trigger-Level Analysis limits from [https://www.hepdata.net/record/ins2966134](https://www.hepdata.net/record/ins2966134).

Different benchmark choices are configured in `modules.benchmarks.benchmarks`. The benchmark used for the re-interpretation examples corresponds to a minimal dark photon model (from a Hidden Abelian Higgs Model)

> Note: for dijet resonance search re-interpretations a complete example workflow is provided in `run_example.sh` and the output can be plotted with `plotting/dark_photon_summary_plots.ipynb`.

### Limit rescaling to different benchmarks
Before doing the dark photon re-interpretation, the limits provides in `inputs` get converted from the simplified model benchmark used for the search to one of the coupling benchmarks configured in `modules.benchmarks.benchmarks`. 

This process uses the `DMWG-couplingScan-code` submodule to re-scale the limits to a different coupling and dark matter mass scenario. 

To rescale dijet resonance search limits use `modules/dijet_rescaling.py`. For further information on the usage of this script run `python modules/dijet_rescaling.py -h`. The script creates some validation plots showing the exclusion depths (defined in [arXiv:2203.12035](https://arxiv.org/abs/2203.12035)) in the $g_q$ vs. $m_{Z'}$ plane along with a comparison of the original and rescaled $g_q$ limits. Examples are shown in:
- Exclusion depth plot: `outputs/TLADijetRun2_J100_observed_validation.pdf`
- Comparison of original and rescaled limits: `outputs/TLADijetRun2_J100_observed_rescaledVector_rescaled_limits.pdf`

Some helper modules have been added to obtain the rescaled exclusion limits in different benchmark scenarios. The `modules/exclusion_helpers.py` module contains classes and helper functions used in `modules/dijet_rescaling.py` to evaluate the rescaled coupling limit.

> Note: the code is not yet setup to handle mono-X limits (e.g. mono-jet or mono-photon), but this is possible to add in the future with a `modules/monox_rescaling.py` module. An example of the rescaling for mono-X final states was provided in the original implementation of the coupling scan code in `DMWG-couplingScan-code/test/monophoton_test.py`. This relies on LHAPDF, which needs to be installed via `conda` in the environment used for these studies [already included in the environment by default].

The output of this stage of the re-interpretation consists of a json file of the form:
```
{
    "mmed_contours": [< list of disconnected exclusion contour x-values >],
    "gq_contours":   [< list of disconnected exclusion contour y-values >],
    "benchmark": <name of the benchmark in modules.benchmarks.benchmarks used for this exclusion contour>
}
```

### Analytical re-interpretation to dark photon models

The dark photon interpretation is based on [arXiv:2206.03456](https://www.arxiv.org/abs/2206.03456) and Section 2.1.1.3
from [arXiv:2405.13778](https://www.arxiv.org/abs/2405.13778) using the re-scaling equation from [arXiv:2405.13778](https://www.arxiv.org/abs/2405.13778).

The `modules/dark_photon.py` script takes the output from the previous step and converts the quark coupling limit to a limit on $\epsilon$, the dark photon mixing parameter. The script outputs a json file storing the dark photon yield parameter $y = \epsilon^2 \cdot \alpha_D \cdot (m_{\mathrm{DM}}/m_{Z'})^4$ and $\epsilon$ separately for all the exclusion contours. To check the usage for the script run `python modules/dark_photon.py -h`.

Example outputs are provided in `outputs/TLADijetRun2_*_darkPhoton.json`.

### Plotting

The `plotting` directory stores the plotting code used to create summary plots stored in `outputs/*_summary_plot.pdf`. At present, this consists of a single notebook that plots the results of the ATLAS Run 2 Trigger-Level Analysis dijet resonance search.

## Credits

This code was developed by Maximilian Amerl, following instructions by Philip C. Harris in [this talk](https://indico.cern.ch/event/1085710/contributions/4564882/attachments/2333706/3977472/PCH_PBC_24_10.pdf) and [this talk](https://indico.cern.ch/event/1554954/contributions/6581184/attachments/3095485/5483694/PCH_Interpret_DM_30_6.pdf) and it was validated against the results obtained by Joshua Greaves [see Master's thesis](https://lup.lub.lu.se/student-papers/search/publication/9091336).
