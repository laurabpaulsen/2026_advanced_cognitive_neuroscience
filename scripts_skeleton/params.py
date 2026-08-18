from pathlib import Path

# PATHS
ROOT = Path("/work")
RAW_PATH = ROOT / "raw"


# determining the user to find a nice place to save derivatives 
p = Path(__file__)

uCloud_user = next(
    part for part in p.parts
    if "#" in part and part.split("#")[1].isdigit()
)


DERIVATIVES_PATH = ROOT / uCloud_user / "derivatives"

if not DERIVATIVES_PATH.exists():
    DERIVATIVES_PATH.mkdir(parents=True)
    print(f"Could not find derivatives path. It has been created at {DERIVATIVES_PATH}")


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


