"""

Script to rescale dijet coupling limits from one simplified model 
benchmark to another using the DMWG-couplingScan-code.

"""
import sys
import matplotlib.pyplot as plt
import mplhep as hep
import argparse
import json
import numpy as np
import pathlib
from modules.benchmarks import benchmarks
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
    Extract closed exclusion contours at exclusion_depth == 1 from the provided
    (mmed, gq) grid and exclusion depth values.

    Parameters
    ----------
    validation_plot_file : pathlib.Path or str
        Path to the validation plot file used for contour extraction (passed to
        the contour extraction routine for plotting/validation).
    mmed : np.ndarray
        1D array of mediator masses (length M).
    gq : np.ndarray
        1D array of quark couplings (length N).
    exclusion_depths : np.ndarray
        Array of exclusion depths evaluated on the (mmed, gq) grid. Expected
        shape is either (M, N) or flattened to length M*N.

    Returns
    -------
    tuple[list, list]
        Tuple (exclusion_x, exclusion_y) where each element is a list of 1D
        numpy arrays. Each pair exclusion_x[i], exclusion_y[i] gives the
        coordinates (mmed, gq) of a single closed exclusion contour at
        exclusion_depth == 1.
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
        "--benchmark",
        type=str,
        required=True,
        help="Name of the benchmark defining the target simplified model.",
        choices=list(benchmarks.keys()),
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
            return 1
        
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
    try:
        gdm_source = src_info["gdm"]
        gl_source = src_info["gl"]
        coupling_source = src_info["coupling"]
        pdfset = src_info["pdfset"]
        ecm_tev = src_info["ecm_sqrt"] / 1e3 # convert to TeV
    except KeyError as e:
        logger.error("Missing key %s in source model info file %s", str(e), str(args.source_info))
        return 1
    
    # get the target benchmark parameters
    benchmark_mdm_fraction = benchmarks[args.benchmark]["parameters"]["mdm_fraction"]
    mdm_model = benchmark_mdm_fraction * mmed
    coupling_model = benchmarks[args.benchmark]["parameters"]["coupling"]
    gdm_model = benchmarks[args.benchmark]["parameters"]["gdm"]
    gl_model = benchmarks[args.benchmark]["parameters"]["gl"]

    # calculate the exclusion depths in the target model
    exclusion_depths = get_coupling_limit_exclusion_depth(
        mmed=mmed,
        mdm_model=mdm_model,
        mdm_source=mdm_source,
        gq_limit=gq_limit,
        coupling_model=coupling_model,
        coupling_source=coupling_source,
        gdm_model=gdm_model,
        gl_model=gl_model,
        gdm_source=gdm_source,
        gl_source=gl_source,
        ecm_tev=ecm_tev,
        pdfset=pdfset
    )

    # extract the rescaled exclusion contours
    exclusion_x, exclusion_y = compute_rescaled_exclusion(
        validation_plot_file=args.validation_plots,
        mmed=mmed,
        gq=GQ_SCAN_VALUES,
        exclusion_depths=exclusion_depths.reshape((len(mmed), len(GQ_SCAN_VALUES)))
    )

    # plot the rescaled limits
    plot_rescaled_limit(
        args.output_file.stem + "_rescaled_limits.pdf",
        exclusion_x,
        exclusion_y,
        args.benchmark,
    )

    # save the rescaled exclusion contours to a json file
    output_data = dict()
    output_data["contour_x"] = [exclusion_xi.tolist() for exclusion_xi in exclusion_x]
    output_data["contour_y"] = [exclusion_yi.tolist() for exclusion_yi in exclusion_y]
    output_data["benchmark"] = args.benchmark
    with open(args.output_file, "w") as f:
        json.dump(output_data, f, indent=4)

    return 0

if __name__ == "__main__":
    sys.exit(main())