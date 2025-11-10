conda deactivate 
conda activate dmwg-coupling-scan

# source the setup script
TOP_LEVEL_DIR=$(cd .. && pwd)
DMWG_COUPLING_SCAN_DIR=$TOP_LEVEL_DIR/DMWG-couplingScan-code

source $DMWG_COUPLING_SCAN_DIR/setup.sh

