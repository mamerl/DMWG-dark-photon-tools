# DMWG Run 3 interpretations

This repository contains a collection of code and setup instructions for different packages. The code is heavily based on interpretations for Run 3 ATLAS dijet searches, but it could be adapted for other signatures (e.g. mono-X, etc.).

For steps in the interpretation that rely on re-scaling DMsimp_s_spin1 model limits, the DMWG-couplingScan-code is used. You can use that code to convert your limits into something expected for the dark photon interpretation code (`dark_photon.py`). The `dark_photon.py` script assumes that your input limit corresponds to a model with $g_{\mathrm{DM}} = 1$ and $g_{\ell} = 0$ for a vector Z' mediator.

> Note: the current version of the DMWG-couplingScan-code submodule points to Max Amerl's personal fork of the DMWG project. This will be updated in the future after some changes are added to the central DMWG project.

## Installation and setup

To run the code a basic conda installation is needed. **First make sure you have conda installed on your laptop or cluster.` If you cannot install conda on a cluster but you have sufficient disk space miniconda is another option: https://www.anaconda.com/docs/getting-started/miniconda/main.

The environment (packages, etc.) needed are outlined in `environment.yml`, including LHAPDF, which is required by DMWG-couplingScan-code. For first time use, run `source install.sh` to setup an environment (it will be called `dmwg-coupling-scan`). For future work just run `source setup.sh` to setup the environment again.

More information on LHAPDF installation is included in the DMWG-couplingScan-code repository in case you prefer another installation procedure.

## Dark photon interpretations

The dark photon interpretation is based on [arXiv:2206.03456](https://www.arxiv.org/abs/2206.03456) and Section 2.1.1.3
from [arXiv:2405.13778](https://www.arxiv.org/abs/2405.13778) using the re-scaling equation from [arXiv:2405.13778](https://www.arxiv.org/abs/2405.13778).

The script handling the rescaling is `modules/dark_photon.py`. To run this you need a json input of the form:
```
{
    "mmed": [...], // Mediator mass
    "mdm": [...], // DM mass
    "gq_limit": [...] // quark coupling limit
}
```
an example is provided in `inputs/example_input.json` based on the rescaled ATLAS Run 2 dijet TLA limit from [https://www.hepdata.net/record/ins2966134](https://www.hepdata.net/record/ins2966134).

The code parses your input and then simply rescales the quark coupling limit to obtain a limit on the dark photon yield parameter $y = \epsilon^2 \cdot \alpha_D \cdot (m_{\mathrm{DM}}/m_{Z'})^4$.

The example can be run with:
```
python modules/dark_photon.py -i inputs/example_input.json -o outputs/example_output.json -gdm 1
```
and you can find the output in `outputs/example_output.*` consisting of the json output and a plot of the resulting limit.