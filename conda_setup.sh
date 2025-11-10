conda deactivate 
conda activate dmwg-coupling-scan

# add this directory to the PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# source the setup script
DMWG_COUPLING_SCAN_DIR=$(pwd)/DMWG-couplingScan-code
cd $DMWG_COUPLING_SCAN_DIR
source setup.sh # this will setup additional LHAPDF environment variables