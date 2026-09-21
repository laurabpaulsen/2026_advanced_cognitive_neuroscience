"""
"""
import mne
from params import fnames, SRC_SPACING, VOL_SPACING, DATES
from utils.argparser import setup_argparser
from utils.logger import setup_report, save_report

import mne
import matplotlib.pyplot as plt
import numpy as np
from mne.transforms import apply_trans


def plot_3d_surface_alignment(info, bem_file, trans, surfaces=["head"], save_path=None):
    """
    Save a 3D matplotlib plot of sensors and head surfaces.
    """
    # Load BEM surfaces
    surf = mne.read_bem_surfaces(bem_file)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})
    axes = axes.flatten()

    # change the perspective to better visualize the alignment for each of the three views
    axes[0].view_init(elev=20, azim=30) 
    axes[1].view_init(elev=20, azim=120)
    axes[2].view_init(elev=20, azim=210)

    # set equal aspect ratio for all axes
    for ax in axes:
        ax.set_box_aspect([1,1,1])


    # Plot surfaces
    surface_descriptions = {"brain": 1, "skull": 2, "head": 4}
    surface_descriptions_to_plot = {desc: id for desc, id in surface_descriptions.items() if desc in surfaces}

    for s in surf:
        if s['id'] not in surface_descriptions_to_plot.values():
            continue

        verts = s['rr'] 
        for ax in axes:
            ax.scatter(verts[:,0], verts[:,1], verts[:,2],
                        s=1, alpha=0.5, label=f"{[k for k,v in surface_descriptions_to_plot.items() if v == s['id']][0]} surface")


    # Plot MEG sensors
    meg_picks = mne.pick_types(info, meg=True, eeg=False)
    sensor_coords = np.array([info['chs'][i]['loc'][:3] for i in meg_picks])

    sensor_coords_mri = apply_trans(info['dev_head_t'], sensor_coords)
    sensor_coords_mri = apply_trans(trans, sensor_coords_mri)
    for ax in axes:
        ax.scatter(sensor_coords_mri[:,0], sensor_coords_mri[:,1], sensor_coords_mri[:,2],
               c='forestgreen', s=15, label='MEG sensors')

    for ax in axes:
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        ax.set_zlabel("Z (m)")
        if ax == axes[-1]:
            ax.legend()

    fig.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=150)

    return fig


if __name__ == "__main__":
    parser = setup_argparser(description="Set up forward models for a given subject.", subject=True)
    args = parser.parse_args()
    subject = args.subject
    
    date = DATES.get(subject, None)
    if date is None:
        raise ValueError(f"No recording date defined for {subject}. Make sure to add it to the DATES dictionary in the params.py file")


    # ------------------------------------------------------------------
    # Create anatomy report
    # ------------------------------------------------------------------
    report_path = fnames.anatomy_report(subject=subject)
    report = setup_report(report_path, title=f"Anatomy Report | {subject}")
    
    # ------------------------------------------------------------------
    # Load needed information 
    # ------------------------------------------------------------------

    # TODO: Read bem solution, 
    # TODO: Read head to mri transformation obtained using the coregistration GUI
    # TODO: read info to get device information (you can use mne.io.read_info)


    # ------------------------------------------------------------------
    # Plot alignment
    # ------------------------------------------------------------------
    fig = plot_3d_surface_alignment(info, fnames.bem_sol(subject=subject), trans, surfaces=["head"])
    report.add_figure(fig, title="3D surface alignment", caption="Alignment of MEG sensors with surfaces.", section="Anatomy", replace=True)


    # ------------------------------------------------------------------
    # Computing forward(s)
    # ------------------------------------------------------------------
    # TODO: Load source space(s)
    # TODO: Compute forward solution(s)
    # TODO: Save forward solution(s)

    # TODO add forward(s) to report

    # ------------------------------------------------------------------
    # Save report
    # ------------------------------------------------------------------
    save_report(report, report_path)