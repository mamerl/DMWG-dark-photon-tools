"""

Script performing conversion of DMSimp model
constraints to dark photon model constraints
based on arXiv:2206.03456 and Section 2.1.1.3
from arXiv:2405.13778

"""
import numpy as np
import json
import pathlib
import sys
import matplotlib.pyplot as plt
import mplhep as hep
from modules.logger_setup import logger
from modules.benchmarks import benchmarks

# See https://pdg.lbl.gov/2025/reviews/rpp2024-rev-phys-constants.pdf
Z_MASS = 91.1880 # GeV
SIN2_THETA_W = 0.23129 # dimensionless
ALPHA_FINE_STRUCTURE = 1/137.035999084 # dimensionless

# new calculation follows https://arxiv.org/pdf/2405.13778 
# see section 2.1.1.3
# TODO revise this calculation after feedback on the derivation of the formula
def calculate_epsilon(mmed:np.ndarray, gq:np.ndarray)->np.ndarray:
    avg_Q2 = 1./3. # approximate
    avg_Y2 = 13./18. # approximate 

    delta_z = (mmed / Z_MASS)**2
    cos2_theta_w = 1. - SIN2_THETA_W
    electronic_charge = np.sqrt(4. * np.pi * ALPHA_FINE_STRUCTURE)

    prefactor =  1. / (electronic_charge * (1. / cos2_theta_w) * (1. / np.abs(1. - delta_z)) * ((np.sqrt(avg_Q2) * cos2_theta_w) + (delta_z * np.sqrt(avg_Y2))))
    epsilon = gq * prefactor
    return epsilon

def compute_yield_parameter(mmed:np.ndarray, mdm:np.ndarray, gq:np.ndarray, gdm:float=1.0)->np.ndarray:
    # safety check for input shapes
    assert mmed.shape == mdm.shape == gq.shape, "mmed, mdm and gq arrays must have the same shape"
    # compute the yield parameter y = epsilon^2 * alpha_D * (m_DM/m_med)^4
    epsilon_coupling = calculate_epsilon(mmed, gq)
    alpha_D = gdm**2 / (4. * np.pi)
    yield_parameter = (epsilon_coupling**2) * alpha_D * (mdm / mmed)**4
    return yield_parameter

def get_arguments():
    import argparse
    parser = argparse.ArgumentParser(
        description="Convert DMSimp limits to dark photon limits",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--benchmark",
        type=str,
        help="Name of the benchmark defining the target simplified model.",
        choices=list(benchmarks.keys()),
        default="minimal_dark_photon",
    )
    parser.add_argument(
        "-i", "--inputfile", 
        type=pathlib.Path, 
        required=True, 
        help="Input JSON file containing DMSimp limits"
    )
    parser.add_argument(
        "-o", "--outputfile", 
        type=pathlib.Path, 
        required=True, 
        help="Output JSON file to store dark photon limits"
    )
    return parser.parse_args()

def main():
    args = get_arguments()

    if not args.inputfile.exists():
        logger.error("input file %s does not exist!", str(args.inputfile))
        return 1
    
    if args.outputfile.exists():
        logger.warning("output file %s already exists, it will be overwritten!", str(args.outputfile))
    
    # load the input file
    input_data = dict()
    with open(args.inputfile, "r") as input_file:
        input_data = json.load(input_file)

    for key in ["mmed_contours", "gq_contours"]:
        if key not in input_data:
            logger.error("input file does not contain required key '%s'", key)
            return 1
    
    mmed = [np.array(contour) for contour in input_data["mmed_contours"]]
    gq_limit = [np.array(contour) for contour in input_data["gq_contours"]]

    # determine how to calculate mdm from the benchmark parameters
    mdm_frac = benchmarks[args.benchmark]["parameters"]["mdm_fraction"]
    mdm = [
        np.array(mmed_contour) * mdm_frac for mmed_contour in mmed
    ]

    # retrieve gdm from the benchmark parameters
    gdm = benchmarks[args.benchmark]["parameters"]["gdm"]
    
    # compute the dark photon limits
    eps_limit = []
    y_limit = []
    for mmed_contour, gq_contour, mdm_contour in zip(mmed, gq_limit, mdm):
        assert mmed_contour.shape == gq_contour.shape, "mmed and gq_limit contours must have the same shape"
        eps_limit.append(calculate_epsilon(mmed_contour, gq_contour).tolist())
        y_limit.append(compute_yield_parameter(mmed_contour, mdm_contour, gq_contour, gdm=gdm).tolist())

    # package the output
    output_data = dict()
    output_data["input"] = str(args.inputfile)
    output_data["mmed"] = [contour.tolist() for contour in mmed]
    output_data["epsilon_limit"] = eps_limit
    output_data["y_limit"] = y_limit

    # write the output file
    logger.info("writing output to %s", str(args.outputfile))
    with open(args.outputfile, "w") as output_file:
        output_file.write(json.dumps(output_data, indent=4, allow_nan=True))

    return 0

if __name__ == "__main__":
    sys.exit(main())
