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

# See https://pdg.lbl.gov/2025/reviews/rpp2024-rev-phys-constants.pdf
Z_MASS = 91.1880 # GeV
SIN2_THETA_W = 0.23129 # dimensionless
ALPHA_FINE_STRUCTURE = 1/137.035999084 # dimensionless

# new calculation follows https://arxiv.org/pdf/2405.13778 
# see section 2.1.1.3
def calculate_epsilon(mmed:np.ndarray, gq:np.ndarray)->np.ndarray:
    avg_Q2 = 0.3 # approximate
    avg_Y2 = 0.7 # approximate

    delta_z = (mmed / Z_MASS)**2
    cos2_theta_w = 1. - SIN2_THETA_W
    electronic_charge = np.sqrt(4. * np.pi * ALPHA_FINE_STRUCTURE)

    prefactor =  1. / (electronic_charge * (1. / cos2_theta_w) * (1. / (1. - delta_z)) * ((np.sqrt(avg_Q2) * cos2_theta_w) + (delta_z * np.sqrt(avg_Y2))))
    epsilon = gq * prefactor
    return epsilon

def compute_cms_yield_parameter(mmed:np.ndarray, mdm:np.ndarray, gq:np.ndarray, gdm:float=1.0)->np.ndarray:
    # safety check for input shapes
    assert mmed.shape == mdm.shape == gq.shape, "mmed, mdm and gq arrays must have the same shape"
    # compute the yield parameter y = epsilon^2 * alpha_D * (m_DM/m_med)^4
    epsilon_coupling = calculate_epsilon(mmed, gq)
    alpha_D = gdm**2 / (4. * np.pi)
    yield_parameter = (epsilon_coupling**2) * alpha_D * (mdm / mmed)**4
    return yield_parameter

def quick_plot(limit_x, limit_y, plot_file:str):

    # initialise plot
    hep.style.use("ATLAS")
    fig, ax = plt.subplots(figsize=(8,6))

    # plot the limit
    ax.plot(limit_x, limit_y)

    # format the axes
    ax.set_yscale("log")
    ax.set_xlabel(r"$m_{Z'}$ [GeV]")
    ax.set_ylabel(r"$y = \epsilon^2 \cdot \alpha_D \cdot (m_{\mathrm{DM}}/m_{Z'})^4$")

    plt.savefig(plot_file)
    plt.close(fig)

    return

def get_arguments():
    import argparse
    parser = argparse.ArgumentParser(
        description="Convert DMSimp limits to dark photon limits",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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
    parser.add_argument(
        "-gdm", "--gdm",
        type=float,
        default=1.0,
        help="Dark matter coupling g_DM"
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

    for key in ["mmed", "mmed", "gq_limit"]:
        if key not in input_data:
            logger.error("input file does not contain required key '%s'", key)
            return 1
    
    mdm = np.array(input_data["mdm"])
    mmed = np.array(input_data["mmed"])
    gq_limit = np.array(input_data["gq_limit"])
    gdm = args.gdm

    # compute the dark photon limits
    dp_limit = compute_cms_yield_parameter(mmed, mdm, gq_limit, gdm=gdm)

    # package the output
    output_data = dict()
    output_data["input"] = str(args.inputfile)
    output_data["mmed"] = mmed.tolist()
    output_data["epsilon_limit"] = dp_limit.tolist()

    # make a quick plot
    quick_plot(mmed, dp_limit, args.outputfile.with_suffix(".pdf").as_posix())

    # write the output file
    with open(args.outputfile, "w") as output_file:
        output_file.write(json.dumps(output_data, indent=4, allow_nan=True))

    return 0

if __name__ == "__main__":
    sys.exit(main())
