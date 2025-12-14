"""

Script to rescale dijet coupling limits from one simplified model 
benchmark to another using the DMWG-couplingScan-code.

"""

import matplotlib.pyplot as plt
import mplhep as hep
import argparse
import json
import numpy as np
import pathlib
from modules.exclusion_helpers import CouplingLimitCalculator
from modules.logger_setup import logger
from couplingscan.limitparsers import CouplingLimit_Dijet
import couplingscan.scan as scan

# NOTE: change these depending on what limits you want to rescale
# your target model should have a coupling limit range defined 
# by [GQ_SCAN_LOW, GQ_SCAN_HIGH] otherwise you will not find
# an exclusion contour in exclusion depth(=1)
GQ_SCAN_LOW = 0.1
GQ_SCAN_HIGH = 0.2
GQ_SCAN_VALUES = np.linspace(GQ_SCAN_LOW, GQ_SCAN_HIGH, 51)

def convert_to_numpy(data)->np.ndarray:
    if isinstance(data, list):
        return np.array(data)
    elif isinstance(data, np.ndarray):
        return data
    elif isinstance(data, (int, float)):
        return np.array([data])
    else:
        raise ValueError("Input data type not supported for conversion to numpy array.")

def get_coupling_limit_exclusion_depth(
    mmed:np.ndarray, # mediator masses for coupling limit points
    mdm_model:np.ndarray,
    mdm_source:np.ndarray,
    gq_limit:np.ndarray, 
    coupling_model:str, 
    coupling_source:str, 
    gdm_model:float=1.0, 
    gl_model:float=0.0, 
    gdm_source:float=1.0, 
    gl_source:float=0.0,
    ecm_tev:float=13.0, # CM frame energy in TeV (i.e. sqrt(s))
    # NOTE the pdfset should only be needed for monojet 
    # rescaling but we configure it for completeness
    pdfset:str='NNPDF31_nnlo_as_0118' # PDF set name
)->np.ndarray:
    """
    Compute the exclusion depth for rescaling the quark coupling limits.

    Parameters
    ----------
    mmed : np.ndarray
        Array of mediator masses.
    mdm_model : np.ndarray
        Array of dark matter masses for the target model (same length as mmed).
    mdm_source : np.ndarray
        Array of dark matter masses for the source model (same length as mmed).
    gq_limit : np.ndarray
        Array of original quark coupling limit points corresponding to mmed.
    coupling_model : str
        Coupling structure of the target model ('vector' or 'axial').
    coupling_source : str
        Coupling structure of the source model ('vector' or 'axial').
    gdm_model : float or array_like, optional
        Dark matter coupling in the target model. Default 1.0.
    gl_model : float or array_like, optional
        Lepton coupling in the target model. Default 0.0.
    gdm_source : float, optional
        Dark matter coupling in the source model. Default 1.0.
    gl_source : float, optional
        Lepton coupling in the source model. Default 0.0.
    ecm_tev : float, optional
        Center-of-mass energy in TeV (sqrt(s)). Default 13.0.
    pdfset : str, optional
        Name of PDF set to use (used for monojet). Default 'NNPDF31_nnlo_as_0118'.

    Returns
    -------
    np.ndarray
        Array of exclusion depths corresponding to mmed (shape matches mmed).

    Raises
    ------
    AssertionError
        If input arrays have incompatible lengths or invalid coupling types.
    """

    # cross-check inputs
    assert coupling_model in ['vector', 'axial'], "coupling_model must be 'vector' or 'axial'"
    assert coupling_source in ['vector', 'axial'], "coupling_source must be 'vector' or 'axial'"
    assert len(mmed) == len(gq_limit), "mmed and gq_limit must have the same length"
    assert len(mdm_model) == len(mmed), "mdm_model and mmed must have the same length"
    assert len(mdm_source) == len(mmed), "mdm_source and mmed must have the same length"
    
    # initialise exclusion depths array
    exclusion_depths = np.zeros_like(mmed)

    # define the coupling limit object for the source model
    coupling_limit = CouplingLimit_Dijet(
        mmed=mmed,
        gq_limits=gq_limit,
        mdm=mdm_source,
        gdm=gdm_source,
        gl=gl_source,
        coupling=coupling_source,
        ECM=(ecm_tev*1e3)**2,
        pdfset=pdfset
    )

    # build the arguments for the scan object in a arguments
    # dictionary
    scan_args = dict()
    scan_args["pdfset"] = coupling_limit.pdfset
    scan_args["ecm"] = coupling_limit.ECM

    # the source limit corresponds to fixed values of 
    # (gq_limit, gdm, gl) vs. mmed
    # for the scan we want to vary gq and fix (gdm, gl)
    gdm_model_array = convert_to_numpy(gdm_model)
    gl_model_array = convert_to_numpy(gl_model)
    
    # obtain a meshgrid of points to be scanned over
    gq_scan, gdm_scan, gl_scan = np.meshgrid(GQ_SCAN_VALUES, gdm_model_array, gl_model_array)
    # set initial values to be reshaped
    scan_args["gq"] = gq_scan.flatten()
    scan_args["gdm"] = gdm_scan.flatten()
    scan_args["gl"] = gl_scan.flatten()
    num_couplings = len(scan_args["gq"]) # original number of coupling points scanned

    # for every set of couplings repeat the couplings for all mmed points to properly
    # scan the coupling v.s. mass parameter space
    scan_args["gq"] = np.matlib.repmat(scan_args["gq"], len(scan_args["mmed"]), 1).reshape((len(scan_args["gq"])*len(scan_args["mmed"]),))
    scan_args["gl"] = np.matlib.repmat(scan_args["gl"], len(scan_args["mmed"]), 1).reshape((len(scan_args["gl"])*len(scan_args["mmed"]),))
    scan_args["gdm"] = np.matlib.repmat(scan_args["gdm"], len(scan_args["mmed"]), 1).reshape((len(scan_args["gdm"])*len(scan_args["mmed"]),))
    scan_args["mmed"] = np.repeat(scan_args["mmed"], num_couplings)
    scan_args["mdm"] = np.repeat(scan_args["mdm"], num_couplings)

    # define a scan object used to compute the exclusion depth
    # in the target model
    scan_handler = None
    if coupling_model == "vector":
        scan_handler = scan.DMVectorModelScan(**scan_args)
    elif coupling_model == "axial":
        scan_handler = scan.DMAxialModelScan(**scan_args)

    # calculate the exclusion depth using the scan object and the 
    # limit parser
    exclusion_depths = scan_handler.extract_exclusion_depths(scan_handler)

    return exclusion_depths


def compute_rescaled_exclusion(validation_plot_file:pathlib.Path, mmed:np.ndarray, gq:np.ndarray, exclusion_depths:np.ndarray)->tuple[list, list]:
    """
    Extract an exclusion contour in the mmed-gq plane corresponding to the contours
    with exclusion_depths == 1.

    Args:
        mmed (np.ndarray): mediator masses array
        gq (np.ndarray): quark coupling array
        exclusion_depths (np.ndarray): exclusion depths array

    Returns:
        tuple[list, list]: tuple of lists of arrays corresponding to closed exclusion contours.
    """

    # define the coupling limit calculator object
    # use dummy values for mdm, gdm, gl as these are not needed
    limit_calculator = CouplingLimitCalculator(
        mmed, 
        mdm=np.zeros_like(mmed), # dummy values for mdm
        gq=gq, 
        gdm=np.zeros_like(mmed), # dummy values for gdm
        gl=np.zeros_like(mmed), # dummy values for gl
        exclusion_depth=exclusion_depths
    )
    # compute the exclusion contour
    exclusion_x, exclusion_y = limit_calculator.compute_exclusion(
        validation_plot_file=str(validation_plot_file), 
        xaxis="mmed", 
        yaxis="gq", 
        exclusion_point=1.0
    )

    return exclusion_x, exclusion_y

def plot_rescaled_limit():
    pass

def get_args():
    parser = argparse.ArgumentParser(
        description="Rescale dijet coupling limits from one simplified model benchmark to another using the DMWG-couplingScan-code."
    )

    parser.add_argument(
        "-s",
        "--source-limit",
        type=pathlib.Path,
        required=True,
        help="Path to the JSON file containing the source dijet coupling limits."
    )
    parser.add_argument(
        "--source-info",
        type=pathlib.Path,
        required=True,
        help="Path to the JSON file containing the source model information (couplings, masses, etc.)."
    )
    parser.add_argument(
        "--validation-plots",
        type=pathlib.Path,
        required=True,
        help="Path to the validation plot file for the target model (used for contour extraction)."
    )
    parser.add_argument(
        "--output-plot-file",
        type=pathlib.Path,
        required=True,
        help="Path to save the output plot with rescaled limits."
    )
    parser.add_argument(
        "--model-file",
        type=pathlib.Path,
        required=True,
        help="Path to the model file defining the target simplified model."
    )

    parser.add_argument(
        "-o",
        "--output-file",
        type=pathlib.Path,
        required=True,
        help="Path to save the output json file with rescaled limits."
    )

    args = parser.parse_args()
    return args

def main():
    args = get_args()

    # make sure all the input files exist
    for file in [args.source_limit, args.source_info, args.validation_plots, args.model_file]:
        if not file.exists():
            logger.error("Input file %s does not exist!", str(file))

    # load the source limit data
    src_limit = dict()
    with open(args.source_limit, "r") as f:
        src_limit = json.load(f)
    # load the source model info data
    src_info = dict()
    with open(args.source_info, "r") as f:
        src_info = json.load(f)

    # extract the relevant arrays
    mmed = np.array(src_limit["mmed"])
    gq_limit = np.array(src_limit["gq_limit"])
    mdm_source = np.array(src_info["mdm"])

    # load the target model info
    model_info = dict()
    with open(args.model_file, "r") as f:
        model_info = json.load(f)
    
    # setup arguments for exclusion depth calculation


    return

if __name__ == "__main__":
    main()