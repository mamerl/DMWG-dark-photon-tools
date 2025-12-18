import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import mplhep as hep
import matplotlib.colors as mcolors
from matplotlib.backends.backend_pdf import PdfPages
from modules.logger_setup import logger

# imports needed for dataclasses allowing 
# automatic generation of __init__ methods
from dataclasses import dataclass

# imports needed for abstract classes
from abc import (
    ABC, 
    abstractmethod
)

# use any style for plotting
# for convenience we just use the ATLAS style here
hep.style.use("ATLAS")

# simple helper function to calculate the exclusion contour
# given some exclusion depth values and points in a plane
# this is adapted from similar plotting code used for ATLAS 
# DM summaries in the past
def contour_exclusion(x_var, y_var, excl_depth, exclusion_point=1.0, closed_contours=False) -> tuple[list, list]:
    """
    Compute 2D contour segments that represent an exclusion boundary.
    This function computes contour lines (or filled contour boundaries) at a specified
    exclusion level from irregularly sampled 2D data. It returns the contour as a
    pair of lists: each list contains one array of x-coordinates and one array of
    y-coordinates per contour segment. The routine is designed to handle both open
    contours produced by tricontour (default) and closed regions produced by
    tricontourf.
    Parameters
    ----------
    x_var : array-like, shape (N,)
        x coordinates of the samples. Must be one-dimensional and have the same
        length as y_var and excl_depth.
    y_var : array-like, shape (N,)
        y coordinates of the samples. Must be one-dimensional and have the same
        length as x_var and excl_depth.
    excl_depth : array-like, shape (N,)
        Scalar value(s) at each sample indicating the exclusion metric. Contours
        are computed at the threshold given by ``exclusion_point``.
    exclusion_point : float, optional (default=1.0)
        Threshold value at which to draw the exclusion contour. For non-closed
        contours (tricontour) the single level ``[exclusion_point]`` is used. For
        closed contours (tricontourf) the levels ``[0, exclusion_point]`` are used
        to produce filled regions whose outer boundary is extracted.
    closed_contours : bool, optional (default=False)
        If False, use plt.tricontour to compute (potentially open) contour lines.
        If True, use plt.tricontourf to compute filled/closed regions and extract
        their boundaries.
    Returns
    -------
    exclusion_x : list of ndarray
        List of 1-D arrays of x-coordinates for each contour segment. Each element
        corresponds to one continuous path/segment returned by the underlying
        matplotlib Path objects.
    exclusion_y : list of ndarray
        List of 1-D arrays of y-coordinates for each contour segment. The i-th
        element pairs with exclusion_x[i].
    Behavior and edge cases
    -----------------------
    - The function expects matplotlib.pyplot as plt and matplotlib.path.Path (for
      Path.MOVETO codes) to be available in the calling module scope.
    - The function inspects the Path.codes of each contour path and splits vertex
      arrays at MOVETO codes to recover individual continuous segments.
    - If no contour segments are found and the entire plane is considered excluded
      (i.e., all values in ``excl_depth`` are <= ``exclusion_point``) and
      ``closed_contours`` is False, the function constructs a fallback horizontal
      line across the unique sorted values of ``x_var`` at y = min(y_var). This
      handles cases where tricontour does not return a boundary because the whole
      domain lies on the excluded side of the threshold.
    - Warnings are emitted (via the module logger) when empty path segments are
      skipped or when the fallback contour is constructed.
    Notes
    -----
    - Input arrays should be one-dimensional and of equal length; otherwise
      matplotlib.tricontour/tricontourf will raise an error.
    - Returned arrays may have varying lengths depending on the topology of the
      contour(s). The caller should iterate over the returned lists to plot or
      process individual segments.
    Example
    -------
    # (pseudo-code)
    xs, ys = contour_exclusion(x, y, depth, exclusion_point=0.95)
    for seg_x, seg_y in zip(xs, ys):
        plt.plot(seg_x, seg_y, '-')
    """

    exclusion_x = list()
    exclusion_y = list()

    # calculate the exclusion contour
    cn = None
    if not closed_contours:
        cn = plt.tricontour(
            x_var,
            y_var,
            excl_depth,
            levels=[exclusion_point],
        )
    else:
        cn = plt.tricontourf(
            x_var,
            y_var,
            excl_depth,
            levels=[0, exclusion_point],
        )

    for path_segment in cn.get_paths():
        vertices = path_segment.vertices
        codes = path_segment.codes

        if len(vertices) == 0:
            logger.warning("skipping empty path segment!")
            continue

        idx = np.where(codes==Path.MOVETO)[0]
        vertex_segs = np.split(vertices,idx)[1:]

        for seg in vertex_segs:
            exclusion_x.append(seg[:,0])
            exclusion_y.append(seg[:,1])

    # if no contour was found check whether the whole plane is excluded
    if len(exclusion_x) == 0 and np.all(excl_depth) <= exclusion_point and not closed_contours: # this is only necessary when doing non-closed contours
        logger.warning("no exclusion contour found, but all points are excluded, so constructing a contour around the plane edges")
    
        # no need to close the contour 
        # just provide a line constant in y 
        # across the whole plane
        exclusion_x = [np.unique(x_var)]
        exclusion_y = [np.full_like(exclusion_x[0], np.min(y_var))]

    return exclusion_x, exclusion_y

# interface for exclusion limit calculators
@dataclass
class ExclusionLimitCalculator(ABC):
    """
    Base class for computing exclusion limits on dark-matter mediator models.
    This abstract base class collects the common input arrays and validation
    logic required to compute exclusion limits for physics interpretations
    (e.g. mediator mass vs dark-matter mass scans for given couplings). Subclasses
    must implement the compute_exclusion(...) method to provide the concrete
    algorithm that produces new exclusion limits from the provided inputs.
    Attributes
    ----------
    mmed : numpy.ndarray
        Array of mediator masses (m_med). Expected to be numeric and shaped
        consistently with mdm and exclusion_depth according to the rules below.
    mdm : numpy.ndarray
        Array of dark-matter masses (m_dm). Expected to be numeric and shaped
        consistently with mmed and exclusion_depth according to the rules below.
    gq : numpy.ndarray
        Array of quark-mediator couplings (g_q). Can be either:
        - an array with the same shape as mmed/mdm/exclusion_depth (per-point coupling), or
        - a length-1 array (a single coupling value applied to all mass points).
    gdm : numpy.ndarray
        Array of dark-matter--mediator couplings (g_dm). Same shape rules as gq.
    gl : numpy.ndarray
        Array of lepton-mediator couplings (g_l). Same shape rules as gq/gdm.
    exclusion_depth : numpy.ndarray
        Array measuring the current exclusion depth (e.g. significance, cross-section
        ratio, or other metric) for each (mmed, mdm[, couplings]) point. Must be
        shaped consistently with the mass arrays.
    Shape and validation rules
    --------------------------
    - In the typical case where couplings are provided per-point (len(gq) > 1 or
      len(gdm) > 1 or len(gl) > 1), all arrays (mmed, mdm, gq, gdm, gl,
      exclusion_depth) are expected to have exactly the same shape. A mismatch
      results in a ValueError raised during initialization.
    - If the couplings are provided as singletons (e.g. a single gq/gdm/gl value
      intended to apply to all mass points), the class accepts the coupling arrays
      having length 1 while mmed, mdm and exclusion_depth share a common shape.
      Implementations should handle broadcasting of single-value couplings when
      computing new limits.
    Initialization behavior
    -----------------------
    - The __post_init__() method performs shape consistency checks described above.
      If the shapes are invalid, a ValueError("input arrays must have the same shape")
      is raised. This method is intended to run after the object is constructed
      (for example, when used as a dataclass or when explicitly called from an
      __init__ override).
    Abstract API
    ------------
    compute_exclusion(*args, **kwargs) -> Any
        Abstract method that subclasses must implement. It should compute and
        return the new exclusion information (for example updated limits,
        boolean mask of excluded points, or numeric metrics) using the attributes
        provided on the instance. The exact signature and return type depend on the
        concrete implementation and use case.
    Notes
    -----
    - All numeric inputs are expected to be numpy.ndarray-compatible. Subclasses
      may assume numpy semantics (vectorized operations, broadcasting, dtypes).
    - The class focuses on input bookkeeping and validation; numerical logic,
      plotting, I/O, and physics-specific details belong in subclasses or helper
      utilities.
    - When designing subclasses, ensure consistent handling of singleton coupling
      arrays (explicit broadcasting) so behavior is predictable for both per-point
      and global-coupling scenarios.
    Examples
    --------
    Intended usage pattern (conceptual):
        class MyCalculator(ExclusionLimitCalculator):
            def compute_exclusion(self):
                # implement physics-specific computation using self.mmed, self.mdm, ...
        # create instance with numpy arrays and call compute_exclusion()
    """

    mmed: np.ndarray
    mdm: np.ndarray
    gq: np.ndarray
    gdm: np.ndarray
    gl: np.ndarray
    exclusion_depth: np.ndarray

    def __post_init__(self):
        # check that the input arrays have reasonable 
        # dimensions allowing the new limits to be 
        # computed
        invalid_shape = False

        if len(self.gq) > 1 or len(self.gdm) > 1 or len(self.gl) > 1:
            invalid_shape = ~np.all(self.mmed.shape == self.mdm.shape == self.gq.shape == 
                self.gdm.shape == self.gl.shape == self.exclusion_depth.shape)
        else:
            # single coupling is specified, so just check the coupling and mass
            # arrays have the same shape individually
            invalid_shape = np.all(self.mmed.shape == self.mdm.shape == self.exclusion_depth)
            invalid_shape = invalid_shape and np.all(self.gq.shape == self.gdm.shape == self.gl.shape)

        if invalid_shape:
            raise ValueError("input arrays must have the same shape")

    @abstractmethod
    def compute_exclusion(self, *args, **kwargs):
        pass

    # NOTE add more options/methods here as needed

# implementation for 1D coupling vs. mmed limits
@dataclass
class CouplingLimitCalculator(ExclusionLimitCalculator):
    """
    CouplingLimitCalculator
    -----------------------
    High-level utility for computing and visualizing exclusion contours in
    a 2D parameter space defined by a mass-like axis (e.g. mediator mass)
    and a coupling-like axis (e.g. quark coupling). This class extends
    ExclusionLimitCalculator and expects the instance to expose arrays that
    define the sampling of the parameter space and a corresponding
    exclusion depth value at each sampled point.
    Conceptual behaviour
    - Given arrays representing an (x, y) sampling of parameter space and a
        per-point exclusion depth, compute the contour where exclusion depth
        equals a chosen "exclusion_point" and produce a validation plot that
        shows the 2D exclusion depth map with the computed contour overlaid.
    - The method compute_exclusion both returns the contour coordinates and
        writes a validation plot to disk.
    Expected attributes on the instance
    - exclusion_depth: array-like, per-sample exclusion depth (float).
    - mmed, mdm: array-like floats for mediator mass and dark-matter mass,
        respectively (used when xaxis is "mmed" or "mdm").
    - gq, gdm, gl: array-like floats for quark, dark-matter and lepton
        couplings (used when yaxis is "gq", "gdm" or "gl").
    - Any other attributes referenced by xaxis/yaxis must be present.
    Public API
    - compute_exclusion(validation_plot_file: str,
                                            xaxis: str = "mmed",
                                            yaxis: str = "gq",
                                            exclusion_point: float = 1.0) -> tuple[list, list]
    compute_exclusion arguments
    - validation_plot_file (str):
            Path where the generated validation plot will be saved. The method
            will create and close a matplotlib figure and overwrite an existing
            file at this path if present.
    - xaxis (str, default "mmed"):
            Name of the attribute on self to use for the horizontal axis.
            Common values: "mmed", "mdm".
    - yaxis (str, default "gq"):
            Name of the attribute on self to use for the vertical axis.
            Common values: "gq", "gdm", "gl".
    - exclusion_point (float, default 1.0):
            The exclusion-level at which to compute the contour. The internal
            contouring routine is expected to compute the locus where
            exclusion_depth == exclusion_point (or the level that most closely
            matches).
    Return value
    - Tuple of two lists or 1D-array-likes: (exclusion_x, exclusion_y)
        representing the contour coordinates in the chosen (xaxis, yaxis)
        space. These correspond to the plotted red dashed contour.
    Side effects and plotting details
    - A filled contour (tricontourf) of the exclusion depth is produced over
        the provided (x, y) samples using a reversed-Blues colormap with a
        grey baseline for the non-excluded region. A colorbar labeled
        "Exclusion depth d_{ex}" with ticks 0..10 is attached.
    - The computed exclusion contour is plotted as a red dashed line with
        circular markers.
    - The produced figure is saved to validation_plot_file with
        bbox_inches="tight" and the matplotlib figure is closed to free
        resources.
    Errors and edge cases
    - Raises ValueError if the requested xaxis or yaxis does not correspond
        to an attribute on the instance.
    - Assumes that x_variable, y_variable and exclusion_depth are numeric
        array-like and are compatible with matplotlib.tricontourf (e.g. 1D
        arrays of the same length describing scattered sample points). If the
        arrays have incompatible shapes or invalid types, matplotlib or the
        contour routine will raise the corresponding exceptions.
    Implementation notes
    - The method delegates contour computation to an external helper
        function named contour_exclusion(x, y, exclusion_depth,
        exclusion_point=...), which should return (x_contour, y_contour).
    - The default axis labels are LaTeX-formatted (e.g. "$m_{\\mathrm{med}}$",
        "$g_q$") and the mass axis label is suffixed with " [GeV]".
    - The plotting and numerical functionality depends on matplotlib,
        numpy and a colormap; these libraries must be available in the
        runtime environment.
    Example (conceptual)
    - Instantiate a CouplingLimitCalculator (providing required base-class
        initialization and data arrays), then:
            exclusion_x, exclusion_y = calc.compute_exclusion(
                    "validation.png",
                    xaxis="mmed",
                    yaxis="gq",
                    exclusion_point=1.0
            )
            # exclusion_x, exclusion_y can be used for further annotations,
            # comparisons, or saving in numeric form.
    """

    # this method is setup to generalise to any 
    # limit form with mass vs. coupling axes
    # but is currently only implemented for mmed vs. gq limits
    def compute_exclusion(self, validation_plot_file:str, xaxis:str="mmed", yaxis:str="gq", exclusion_point:float=1.0) -> tuple[list, list]:
        # get the variables corresponding to the axes
        # and check they are valid attributes
        x_variable = getattr(self, xaxis, None)
        y_variable = getattr(self, yaxis, None)

        if x_variable is None:
            raise ValueError(f"xaxis '{xaxis}' is not a valid attribute")

        if y_variable is None:
            raise ValueError(f"yaxis '{yaxis}' is not a valid attribute")
        
        # labels for plotting
        y_label = str()
        if yaxis == "gq":
            y_label = r"$g_q$"
        elif yaxis == "gdm":
            y_label = r"$g_{\chi}$"
        elif yaxis == "gl":
            y_label = r"$g_\ell$"
        
        mass_label = str()
        if xaxis == "mmed":
            mass_label = r"$m_{\mathrm{med}}$"
        elif xaxis == "mdm":
            mass_label = r"$m_{\mathrm{DM}}$"

        # calculate the exclusion contour
        exclusion_x, exclusion_y = contour_exclusion(
            x_variable, 
            y_variable, 
            self.exclusion_depth, 
            exclusion_point=exclusion_point,
            # use open contours for coupling vs. mass limits
            # since we probably want limit lines rather than
            # filled regions
            closed_contours=False, 
        )

        # 2D plot showing exclusion depth as a function 
        # of both mass and coupling
        fig, ax = plt.subplots(figsize=(10, 8))
        levels = np.array(
            [0., 1.] + [1. + i*((10. - 1.)/float(100.)) for i in range(1, 101)]
        )
        level_colors = ["tab:grey"] + plt.get_cmap('Blues_r')(np.linspace(0, 1, len(levels)-1)).tolist()
        norm = mcolors.BoundaryNorm(boundaries=levels, ncolors=len(level_colors))
        cp = ax.tricontourf(
            x_variable, 
            y_variable, 
            self.exclusion_depth, 
            levels=levels, 
            colors=level_colors,
            norm=norm,
        )
        # this fills in gaps between levels with contour lines
        ax.tricontour(
            x_variable, 
            y_variable, 
            self.exclusion_depth, 
            levels=levels, 
            colors=level_colors, 
            linewidths=0.5,
            norm=norm,
        )
        cbar = fig.colorbar(cp, ticks=np.linspace(0, 10, 11), boundaries=levels, spacing="proportional", pad=0.02)
        cbar.set_label(r'Exclusion depth $d_{\mathrm{ex}}$')
        cbar.set_ticklabels([str(i) for i in range(0, 11)])
        ax.set_xlabel(mass_label + " [GeV]")
        ax.set_ylabel(y_label)
        
        # plot the new exclusion contour
        for cx, xy in zip(exclusion_x, exclusion_y):
            ax.plot(
                cx, 
                xy, 
                color="red", 
                linestyle="--",
                # marker="o",
                # markersize=7,
                linewidth=1.75,
            )

        plt.savefig(validation_plot_file, bbox_inches="tight")
        plt.close(fig)

        return exclusion_x, exclusion_y