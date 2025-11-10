# DMWG Run 3 interpretations

This repository contains a collection of code and setup instructions for different packages. The code is heavily based on interpretations for Run 3 ATLAS dijet searches, but it could be adapted for other signatures (e.g. mono-X, etc.).

For steps in the interpretation that rely on re-scaling DMsimp_s_spin1 model limits, the DMWG-couplingScan-code is used. You can use that code to convert your limits into something expected for the dark photon interpretation code (`dark_photon.py`).

> Note: the current version of the DMWG-couplingScan-code submodule points to Max Amerl's personal fork of the DMWG project. This will be updated in the future after some changes are added to the central DMWG project.

## Installation and setup

To run the code a basic conda installation is needed. **First make sure you have conda installed on your laptop or cluster.` If you cannot install conda on a cluster but you have sufficient disk space miniconda is another option: https://www.anaconda.com/docs/getting-started/miniconda/main.

The environment (packages, etc.) needed are outlined in `environment.yml`, including LHAPDF, which is required by DMWG-couplingScan-code. For first time use, run `source install.sh` to setup an environment (it will be called `dmwg-coupling-scan`). For future work just run `source setup.sh` to setup the environment again.

More information on LHAPDF installation is included in the DMWG-couplingScan-code repository in case you prefer another installation procedure.

## Running dark photon interpretation

The dark photon interpretation is based on 