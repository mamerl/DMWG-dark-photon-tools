"""

List of benchmarks that can be considered when doing the dark photon
interpretation

Add new benchmarks by adding new entries to the `benchmarks` dictionary below.
Each benchmark is defined by a name (the key in the dictionary) and
a set of parameters (the value in the dictionary) including:
- description: A text description of the benchmark
- parameters: A dictionary of model parameters including:
    - gdm: The dark matter coupling
    - gl: The lepton coupling
    - mdm_fraction: The fraction of the mediator mass that sets the dark matter mass
    - coupling: The type of coupling ("vector" or "axial")

The model parameters are used to convert quark coupling limits on a simplified DM model
mediator (i.e. DMsimp spin-1 s-channel mediator) into limits that can be analytically 
converted into dark photon model parameters.

"""

benchmarks = {
    "minimal_dark_photon": {
        "name": "HAHM Dark Photon",
        "description": "Minimal dark photon model with the DM mass set to a fixed ratio of the mediator (dark photon) mass",
        "parameters": {
            "gdm": 1.0,
            "gl": 0.0,
            "mdm_fraction": 1./3., # mdm = mdm_fraction * mmed
            "coupling": "vector",
        },
        "plot_parameters": {
            "mdm_label": r"$m_{\mathrm{DM}} = m_{Z'}/3$",
            "coupling_label": r"$g_{\mathrm{DM}} = 1.0$, $g_{\ell} = 0.0$",
        }
    }
}