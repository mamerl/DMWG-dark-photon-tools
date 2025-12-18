# Inputs for dark photon interpretations

This directory contains the inputs for the dark photon interpretation code. Two examples from the ATLAS Run 2 Dijet Trigger-Level Analysis search have been provided (available at [https://www.hepdata.net/record/ins2966134](https://www.hepdata.net/record/ins2966134)):
- `TLADijetRun2_*_expected_limit.json`: the original **expected** quark coupling ($g_q$) limit for an axial-vector $Z'$ mediator with model parameters: $m_{\mathrm{DM}} = 10$ TeV, $g_{\ell} = 0$, and $g_{\mathrm{DM}} = 1$.
- `TLADijetRun2_*_observed_limit.json`: the original **observed** quark coupling ($g_q$) limit for an axial-vector $Z'$ mediator with model parameters: $m_{\mathrm{DM}} = 10$ TeV, $g_{\ell} = 0$, and $g_{\mathrm{DM}} = 1$.

Information about the models used for the `TLADijetRun2_*.json` limit files is available in `TLADijetRun2_limit_params.json`. The J50 and J100 files correspond to the different signal regions used ATLAS TLA Run 2 dijet resonance search.

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
