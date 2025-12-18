################################################################
# Run example script for dijet limit rescaling to dark photon  #
################################################################

### Rescale from axial-vector to vector mediator limits with changes
### to DM mass and mediator coupling structure via the DMWG-couplingScan-code
python modules/dijet_rescaling.py -s inputs/TLADijetRun2_J100_observed_limit.json --source-info inputs/TLADijetRun2_limit_params.json --validation-plots outputs/TLADijetRun2_J100_observed_validation.pdf --benchmark minimal_dark_photon -o outputs/TLADijetRun2_J100_observed_rescaledVector.json
python modules/dijet_rescaling.py -s inputs/TLADijetRun2_J50_observed_limit.json --source-info inputs/TLADijetRun2_limit_params.json --validation-plots outputs/TLADijetRun2_J50_observed_validation.pdf --benchmark minimal_dark_photon -o outputs/TLADijetRun2_J50_observed_rescaledVector.json
python modules/dijet_rescaling.py -s inputs/TLADijetRun2_J100_expected_limit.json --source-info inputs/TLADijetRun2_limit_params.json --validation-plots outputs/TLADijetRun2_J100_expected_validation.pdf --benchmark minimal_dark_photon -o outputs/TLADijetRun2_J100_expected_rescaledVector.json
python modules/dijet_rescaling.py -s inputs/TLADijetRun2_J50_expected_limit.json --source-info inputs/TLADijetRun2_limit_params.json --validation-plots outputs/TLADijetRun2_J50_expected_validation.pdf --benchmark minimal_dark_photon -o outputs/TLADijetRun2_J50_expected_rescaledVector.json

### Rescale from vector mediator limits to dark photon limits
python modules/dark_photon.py --benchmark minimal_dark_photon -i outputs/TLADijetRun2_J100_observed_rescaledVector.json -o outputs/TLADijetRun2_J100_observed_darkPhoton.json
python modules/dark_photon.py --benchmark minimal_dark_photon -i outputs/TLADijetRun2_J50_observed_rescaledVector.json -o outputs/TLADijetRun2_J50_observed_darkPhoton.json
python modules/dark_photon.py --benchmark minimal_dark_photon -i outputs/TLADijetRun2_J100_expected_rescaledVector.json -o outputs/TLADijetRun2_J100_expected_darkPhoton.json
python modules/dark_photon.py --benchmark minimal_dark_photon -i outputs/TLADijetRun2_J50_expected_rescaledVector.json -o outputs/TLADijetRun2_J50_expected_darkPhoton.json