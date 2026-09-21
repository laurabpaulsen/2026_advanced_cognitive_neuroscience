import mne

from params import SRC_SPACING, VOL_SPACING, fnames
from utils.argparser import setup_argparser
from utils.logger import setup_report, save_report


if __name__ == "__main__":
    parser = setup_argparser(description="Set up BEM and source spaces for a given subject", subject=True)
    args = parser.parse_args()
    subject = args.subject


    # ------------------------------------------------------------------
    # Create anatomy report
    # ------------------------------------------------------------------
    report_path = fnames.anatomy_report(subject=subject)
    report = setup_report(report_path, title=f"Anatomy Report | {subject}")
    
    # ------------------------------------------------------------------
    # Setup boundary element model (BEM)
    # ------------------------------------------------------------------
    bem_file = fnames.bem_model(subject=subject)
    bem_sol_file = fnames.bem_sol(subject=subject)
    
    # TODO: Make bem model
    # TODO: write bem surfaces to disk


    # TODO: Make bem solution
    # TODO: write bem surfaces to disk

    # TODO: Add to report


    # ------------------------------------------------------------------
    # Set up source space(s). Atleast surface source space, but you can also add volume + combined
    # ------------------------------------------------------------------
    # TODO: Set up surface source space
    # TODO: write to disk

    # TODO: Maybe create volume + combined source spaces?

    # ------------------------------------------------------------------
    # Compute morphs to fsaverage and save
    # ------------------------------------------------------------------
    subject_to = "fsaverage"

    # TODO: load fsaverage source space
    # TODO: Create the morph using mne.compute_source_morph
    # TODO: Save the morph

    # ------------------------------------------------------------------
    # Save report
    # ------------------------------------------------------------------
    save_report(report, report_path)
