# Inputs for dark photon interpretations

This directory contains the inputs for the dark photon interpretation code. Two examples from the ATLAS Run 2 Dijet Trigger-Level Analysis search have been provided (available at [https://www.hepdata.net/record/ins2966134](https://www.hepdata.net/record/ins2966134)):
- `rescaled_example_input.json`: the rescaled quark coupling ($g_q$) limit (from the J100 signal region) corresponding to a vector $Z'$ mediator with $g_{\mathrm{DM}} = 1$ and $g_{\ell} = 0$. This is obtained by running the [DMWG-couplingScan-code](https://github.com/mamerl/DMWG-couplingScan-code/tree/run3-update). **This is intended to be used as a direct input to `modules/dark_photon.py` for testing**
- `TLADijetRun2_J100_expected_limit.json`: the original **expected** quark coupling ($g_q$) limit for an axial-vector $Z'$ mediator with model parameters: $m_{\mathrm{DM}} = 10$ TeV, $g_{\ell} = 0$, and $g_{\mathrm{DM}} = 1$.
- `TLADijetRun2_J100_observed_limit.json`: the original **observed** quark coupling ($g_q$) limit for an axial-vector $Z'$ mediator with model parameters: $m_{\mathrm{DM}} = 10$ TeV, $g_{\ell} = 0$, and $g_{\mathrm{DM}} = 1$.
Information about the models used for the `TLADijetRun2_*.json` limit files is available in `TLADijetRun2_limit_params.json`.

## Preparing input files
To add a new limit you need to create: (1) the limit json file, (2) the limit information file.

The limit json file should have the format:
```
{
    "mmed": [<list of mediator masses for each limit point>],
    "mdm": [<list of DM masses for each limit point>],
    "gq_limit": [<quark coupling limit for each mediator mass>]
}
```

The limit information file should have the format:
```
{
    ["info": "<description of the file>",] # optional description of file
    "gdm": <float DM-mediator coupling>,
    "gl": <float mediator-lepton coupling>,
    "mdm": <DM mass in GeV>,
    "coupling": <coupling type: "axial"/"vector">,
    "ecm_sqrt": <sqrt(s) CM frame energy for the search>,
    "pdfset": <PDF set used to generate signal MC for the limits (used by coupling scan code later)>
}
```
