from pathlib import Path

# PATHS
ROOT = Path("/work")
RAW_PATH = ROOT / "raw"
SUBJECTS_DIR = ROOT / "freesurfer"

# determining the user to find a nice place to save derivatives 
p = Path(__file__)

uCloud_user = next(
    part for part in p.parts
    if "#" in part and part.split("#")[1].isdigit()
)


DERIVATIVES_PATH = ROOT / uCloud_user / "derivatives"
MEG_PATH = DERIVATIVES_PATH / "MEG"

if not MEG_PATH.exists():
    MEG_PATH.mkdir(parents=True)
    print(f"Could not find derivatives path. It has been created at {MEG_PATH}")



# PREPROCESSING PARAMETERS
## list of bad channels for each subject
BAD_CHANNELS = {
    "sub-001": [],
    "sub-002": [],
    #....
    "sub-nnn":[]
}

## Filtering


## Epoching
EPOCHS_TMIN = -0.2
EPOCHS_TMAX = 0.7
BASELINE = (None, 0) # from tmin to time of stimulation
DOWNSAMPLE_RATE = 250


# SOURCE MODELLING
SRC_SPACING = "oct6"
VOL_SPACING = 10