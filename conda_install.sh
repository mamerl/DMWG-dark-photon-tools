#####################################################
#### Generic installation script for setting up the 
#### repository in a conda environment
####
#### This is useful if one wants to retrieve LHAPDF
#### from conda-forge to avoid needing lxplus

# NOTE all the specific configuration info for the environment
# is stored in conda_environment.yml

# update conda to latest version
conda update conda -y

# create conda environment
conda env create -f conda_environment.yml -y

# enter environment
conda activate dmwg-coupling-scan 

# LHAPDF setup 
# install the pdf sets (these will go into the conda environment)
# NOTE: you can add more pdf sets here if needed
lhapdf install NNPDF30_nlo_as_0118
lhapdf install NNPDF30_nlo_as_0118_hessian

# install the DMWG-couplingScan-code package
cd DMWG-couplingScan-code

# install the pybind11 code in src
pip install -e .

# source the setup script for other environment variables
# to be set properly
source setup.sh
