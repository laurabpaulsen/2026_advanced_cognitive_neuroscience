import numpy as np

# stolen from : https://neurowaves.science/6-meg-pipeline-gallery/notebooks/mne/mne_kit_photodiode_pipeline
def rising_edges(x, sf, frac=0.9, refractory_s=0.5):
    lo, hi = np.percentile(x, [1, 99])
    above = x > lo + frac*(hi-lo)
    cand = np.flatnonzero(above[1:] & ~above[:-1]) + 1
    keep = [cand[0]]
    for i in cand[1:]:
        if (i-keep[-1])/sf > refractory_s: keep.append(i)
    return np.asarray(keep, int)




def adjust_timing_of_events_photodiode(raw, events, event_id, photodiode_ch_name = "MISC002", report=None, stim_trigs = [1, 3]):
    """

    """
    
    photodiode_data = raw.get_data(picks=photodiode_ch_name).squeeze()

    photodiode_trigs = rising_edges(photodiode_data, raw.info["sfreq"])
    
    photodiode_trigs = photodiode_trigs + raw.first_samp

    # find the trigger values for the events with photodiode (the gabor patches)
    events_stim = np.array([event for event in events if event[-1] in stim_trigs])

    # compare event timing from photodiode and triggers
    diff = []

    for event in events_stim:
        samp = event[0]
        
        # find the nearest matching photodiode event
        difference = np.abs(photodiode_trigs - samp)
        idx = difference.argmin()
        diff.append(photodiode_trigs[idx]-samp)
        
    # count each of the occurences 
    unique_diff, counts = np.unique(diff, return_counts=True)

    # find the mode
    mode = unique_diff[np.argmax(counts)]
    if report:

        html = f"""
        <h3>Photodiode timing differences</h3>

        <p>
            <strong>Mode (most common difference):</strong>
            {mode} samples
        </p>

        <table style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: center;">
                        Difference (samples)
                    </th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: center;">
                        Count
                    </th>
                </tr>
            </thead>
            <tbody>
        """

        for difference, count in zip(unique_diff, counts):

            # Highlight the mode
            if difference == mode:
                row_style = "background-color: #d9ead3; font-weight: bold;"
            else:
                row_style = ""

            html += f"""
                <tr style="{row_style}">
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">
                        {difference}
                    </td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">
                        {count}
                    </td>
                </tr>
            """

        html += """
            </tbody>
        </table>
        """

        report.add_html(
            html,
            title="Photodiode timing differences",
            replace=True
        )


    adjusted_events = events.copy()
    adjusted_events[:, 0] = adjusted_events[:, 0] + mode

    if report:
        
        plot_duration = 5  # seconds shown in each plot
        n_plots = 10

        recording_duration = raw.n_times / raw.info["sfreq"]

        start_times = np.linspace(
            0,
            recording_duration - plot_duration,
            n_plots
        )

        figures = []

        for start in start_times:

            fig = raw.plot(
                picks=photodiode_ch_name,
                events=adjusted_events,
                start=start,
                duration=5,
                event_id=event_id,
                show=False,
                show_scalebars=False,
                event_color="darkorange",
            )

            figures.append(fig)

        report.add_figure(
            figures,
            title="Triggers after adjusting for delay determined using the photodiode",
            replace=True,
        )

    return adjusted_events
