import numpy as np
import matplotlib.pyplot as plt
import qetpy as qp


__all__ = [
    "plot_full_trace",
    "plot_single_period_of_trace",
    "plot_zoomed_in_trace",
    "plot_didv_flipped",
    "plot_re_im_didv",
    "plot_abs_phase_didv",
]


def _plot_time_domain(didv, poles):
    """Helper function for plotting the fits in time domain."""

    if poles == "all":
        poleslist = np.array([1, 2, 3])
    else:
        poleslist = np.array(poles)

    ## plot the entire trace with fits
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        didv._time * 1e6,
        (didv._tmean - didv._offset) * 1e6,
        color='k',
        label='Mean',
    )

    if (didv._1poleresult is not None) and (1 in poleslist):
        didvfit1_timedomain = qp.squarewaveresponse(
            didv._time,
            didv._rshunt,
            didv._sgamp,
            didv._sgfreq,
            didv._dutycycle,
            **didv._1poleresult['params'],
        )
        ax.plot(
            (didv._time + didv._1poleresult['params']['dt']) * 1e6,
            didvfit1_timedomain * 1e6,
            color='magenta',
            alpha=0.9,
            label='1-Pole Fit',
        )

    if (didv._2poleresult is not None) and (2 in poleslist):
        didvfit2_timedomain = qp.squarewaveresponse(
            didv._time,
            didv._rshunt,
            didv._sgamp,
            didv._sgfreq,
            didv._dutycycle,
            **didv._2poleresult['params'],
        )
        ax.plot(
            (didv._time + didv._2poleresult['params']['dt']) * 1e6,
            didvfit2_timedomain * 1e6,
            color='green',
            alpha=0.9,
            label='2-Pole Fit',
        )

    if (didv._3poleresult is not None) and (3 in poleslist):
        didvfit3_timedomain = qp.squarewaveresponse(
            didv._time,
            didv._rshunt,
            didv._sgamp,
            didv._sgfreq,
            didv._dutycycle,
            **didv._3poleresult['params'],
        )
        ax.plot(
            (didv._time + didv._3poleresult['params']['dt']) * 1e6,
            didvfit3_timedomain * 1e6,
            color='orange',
            alpha=0.9,
            label='3-Pole Fit',
        )

    ax.set_xlabel('Time ($\mu$s)')
    ax.set_ylabel('Amplitude ($\mu$A)')
    ax.legend(loc='upper left')
    ax.grid(linestyle='dotted')
    ax.tick_params(which='both', direction='in', right=True, top=True)

    return fig, ax


def plot_full_trace(didv, poles="all", lgcsave=False, savepath="",
                    savename=""):
    """
    Function to plot the entire trace in time domain

    Parameters
    ----------
    didv : class
        The DIDV class object that the data is stored in
    poles : int, string, array_like, optional
        The pole fits that we want to plot. If set to "all", then plots
        all of the fits. Can also be set to just one of the fits. Can
        be set as an array of different fits, e.g. [1, 2]
    lgcsave : boolean, optional
        Boolean value on whether or not the figure should be saved
    savepath : string, optional
        Where the figure should be saved. Saved in the current
        directory by default.
    savename : string, optional
        A string to append to the end of the file name if saving. Empty
        string by default.

    """

    fig, ax = _plot_time_domain(didv, poles)

    ax.set_xlim([didv._time[0] * 1e6, didv._time[-1] * 1e6])
    ax.set_title("Full Trace of dIdV")

    if lgcsave:
        fig.savefig(savepath + f"full_trace_{savename}.png")
        plt.close(fig)
    else:
        plt.show()


def plot_single_period_of_trace(didv, poles="all", lgcsave=False, savepath="",
                                savename=""):
    """
    Function to plot a single period of the trace in time domain

    Parameters
    ----------
    didv : class
        The DIDV class object that the data is stored in
    poles : int, string, array_like, optional
        The pole fits that we want to plot. If set to "all", then plots
        all of the fits. Can also be set to just one of the fits. Can
        be set as an array of different fits, e.g. [1, 2]
    lgcsave : boolean, optional
        Boolean value on whether or not the figure should be saved
    savepath : string, optional
        Where the figure should be saved. Saved in the current
        directory by default.
    savename : string, optional
        A string to append to the end of the file name if saving. Empty
        string by default.

    """

    fig, ax = _plot_time_domain(didv, poles)

    period = 1.0/didv._sgfreq

    ax.set_xlim([didv._time[0] * 1e6, didv._time[0] * 1e6 + period * 1e6])
    ax.set_title("Single Period of Trace")

    if lgcsave:
        fig.savefig(savepath + f"trace_one_period_{savename}.png")
        plt.close(fig)
    else:
        plt.show()


def plot_zoomed_in_trace(didv, poles="all", zoomfactor=0.1, lgcsave=False,
                         savepath="", savename=""):
    """
    Function to plot a zoomed in portion of the trace in time domain.
    This plot zooms in on the overshoot of the didv._

    Parameters
    ----------
    didv : class
        The DIDV class object that the data is stored in
    poles : int, string, array_like, optional
        The pole fits that we want to plot. If set to "all", then plots
        all of the fits. Can also be set to just one of the fits. Can
        be set as an array of different fits, e.g. [1, 2]
    zoomfactor : float, optional, optional
        Number between zero and 1 to show different amounts of the
        zoomed in trace.
    lgcsave : boolean, optional
        Boolean value on whether or not the figure should be saved
    savepath : string, optional
        Where the figure should be saved. Saved in the current
        directory by default.
    savename : string, optional
        A string to append to the end of the file name if saving.
        Empty string by default.

    """

    period = 1.0 / didv._sgfreq

    cost_lambda = lambda x: x['cost'] if x is not None else None
    dt_lambda = lambda x: x['params']['dt'] if x is not None else None

    cost_vals = [
        cost_lambda(didv._1poleresult),
        cost_lambda(didv._2poleresult),
        cost_lambda(didv._3poleresult),
    ]
    dt_vals = [
        dt_lambda(didv._1poleresult),
        dt_lambda(didv._2poleresult),
        dt_lambda(didv._3poleresult),
    ]
    if all(fv is None for fv in cost_vals):
        best_time_offset = 0
    else:
        min_cost_idx = min(
            (val, ii) for ii, val in enumerate(cost_vals) if val is not None
        )[1]
        best_time_offset = dt_vals[min_cost_idx]

    fig, ax = _plot_time_domain(didv, poles)

    ax.set_xlim(
        (best_time_offset + didv._time[0] + (
            0.5 - zoomfactor / 2
        ) * period) * 1e6,
        (best_time_offset + didv._time[0] + (
            0.5 + zoomfactor / 2) * period
        ) * 1e6,
    )

    ax.set_title("Zoomed In Portion of Trace")

    if lgcsave:
        fig.savefig(savepath + f"zoomed_in_trace_{savename}.png")
        plt.close(fig)
    else:
        plt.show()


def plot_didv_flipped(didv, poles="all", lgcsave=False, savepath="",
                      savename=""):
    """
    Function to plot the flipped trace in time domain. This function
    should be used to test if there are nonlinearities in the didv

    Parameters
    ----------
    didv : class
        The DIDV class object that the data is stored in
    poles : int, string, array_like, optional
        The pole fits that we want to plot. If set to "all", then plots
        all of the fits. Can also be set to just one of the fits. Can
        be set as an array of different fits, e.g. [1, 2]
    lgcsave : boolean, optional
        Boolean value on whether or not the figure should be saved
    savepath : string, optional
        Where the figure should be saved. Saved in the current
        directory by default.
    savename : string, optional
        A string to append to the end of the file name if saving. Empty
        string by default.

    """

    fig, ax = _plot_time_domain(didv, poles)

    period = 1.0 / didv._sgfreq
    time_flipped = didv._time - period / 2.0
    tmean_flipped = -(didv._tmean - didv._offset)

    ax.plot(
        time_flipped * 1e6,
        tmean_flipped * 1e6,
        color='blue',
        label='Flipped Data',
    )

    ax.set_title("Flipped Traces to Check Asymmetry")

    if lgcsave:
        fig.savefig(savepath + f"flipped_trace_{savename}.png")
        plt.close(fig)
    else:
        plt.show()


def plot_re_im_didv(didv, poles="all", lgcsave=False, savepath="",
                    savename=""):
    """
    Function to plot the real and imaginary parts of the didv in
    frequency space. Currently creates two different plots.

    Parameters
    ----------
    didv : class
        The DIDV class object that the data is stored in
    poles : int, string, array_like, optional
        The pole fits that we want to plot. If set to "all", then plots
        all of the fits. Can also be set to just one of the fits. Can
        be set as an array of different fits, e.g. [1, 2]
    lgcsave : boolean, optional
        Boolean value on whether or not the figure should be saved
    savepath : string, optional
        Where the figure should be saved. Saved in the current
        directory by default.
    savename : string, optional
        A string to append to the end of the file name if saving. Empty
        string by default.

    """

    if poles == "all":
        poleslist = np.array([1,2,3])
    else:
        poleslist = np.array(poles)

    ## don't plot points with huge errors
    goodinds = np.abs(didv._didvmean / didv._didvstd) > 2.0
    fitinds = didv._freq > 0
    plotinds = np.logical_and(fitinds, goodinds)

    cost_lambda = lambda x: x['cost'] if x is not None else None
    dt_lambda = lambda x: x['params']['dt'] if x is not None else None

    cost_vals = [
        cost_lambda(didv._1poleresult),
        cost_lambda(didv._2poleresult),
        cost_lambda(didv._3poleresult),
    ]
    dt_vals = [
        dt_lambda(didv._1poleresult),
        dt_lambda(didv._2poleresult),
        dt_lambda(didv._3poleresult),
    ]
    if all(fv is None for fv in cost_vals):
        best_time_offset = 0
    else:
        min_cost_idx = min(
            (val, ii) for ii, val in enumerate(cost_vals) if val is not None
        )[1]
        best_time_offset = dt_vals[min_cost_idx]

    time_phase = np.exp(2.0j * np.pi * best_time_offset * didv._freq)

    ## plot the real part of the dIdV in frequency domain
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        didv._freq[plotinds],
        np.real(didv._didvmean * time_phase)[plotinds],
        color='blue',
        label='Mean',
        s=5,
    )
    ## plot error in real part of dIdV
    ax.plot(
        didv._freq[plotinds],
        np.real((didv._didvmean + didv._didvstd) * time_phase)[plotinds],
        color='black',
        label='1-$\sigma$ Bounds',
        alpha=0.1,
    )
    ax.plot(
        didv._freq[plotinds],
        np.real((didv._didvmean - didv._didvstd) * time_phase)[plotinds],
        color='black',
        alpha=0.1,
    )

    if (didv._1poleresult is not None) and (1 in poleslist):
        didvfit1_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(1)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.real(didvfit1_freqdomain)[fitinds],
            color='magenta',
            label='1-Pole Fit',
        )

    if (didv._2poleresult is not None) and (2 in poleslist):
        didvfit2_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(2)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.real(didvfit2_freqdomain)[fitinds],
            color='green',
            label='2-Pole Fit',
        )

    if (didv._3poleresult is not None) and (3 in poleslist):
        didvfit3_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(3)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.real(didvfit3_freqdomain)[fitinds],
            color='orange',
            label='3-Pole Fit',
        )

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Re($dI/dV$) ($\Omega^{-1}$)')
    ax.set_xscale('log')

    yhigh = max(np.real(
        didv._didvmean * time_phase
    )[plotinds][didv._freq[plotinds] < 1e5])
    ylow = min(np.real(
        didv._didvmean * time_phase
    )[plotinds][didv._freq[plotinds] < 1e5])

    ybnd = np.max([yhigh, -ylow])

    ax.set_ylim([-ybnd, ybnd])
    ax.set_xlim([min(didv._freq[fitinds]), max(didv._freq[fitinds])])
    ax.legend(loc='upper left')
    ax.set_title("Real Part of dIdV")
    ax.tick_params(which='both', direction='in', right=True, top=True)
    ax.grid(which='major')
    ax.grid(which='minor', linestyle='dotted', alpha=0.3)

    if lgcsave:
        fig.savefig(savepath + f"didv_real_{savename}.png")
        plt.close(fig)
    else:
        plt.show()

    ## plot the imaginary part of the dIdV in frequency domain
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        didv._freq[plotinds],
        np.imag(didv._didvmean * time_phase)[plotinds],
        color='blue',
        label='Mean',
        s=5,
    )

    ## plot error in imaginary part of dIdV
    ax.plot(
        didv._freq[plotinds],
        np.imag((didv._didvmean + didv._didvstd) * time_phase)[plotinds],
        color='black',
        label='1-$\sigma$ Bounds',
        alpha=0.1,
    )
    ax.plot(
        didv._freq[plotinds],
        np.imag((didv._didvmean - didv._didvstd) * time_phase)[plotinds],
        color='black',
        alpha=0.1,
    )

    if (didv._1poleresult is not None) and (1 in poleslist):
        didvfit1_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(1)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.imag(didvfit1_freqdomain)[fitinds],
            color='magenta',
            label='1-Pole Fit',
        )

    if (didv._2poleresult is not None) and (2 in poleslist):
        didvfit2_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(2)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.imag(didvfit2_freqdomain)[fitinds],
            color='green',
            label='2-Pole Fit',
        )

    if (didv._3poleresult is not None) and (3 in poleslist):
        didvfit3_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(3)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.imag(didvfit3_freqdomain)[fitinds],
            color='orange',
            label='3-Pole Fit',
        )

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Im($dI/dV$) ($\Omega^{-1}$)')
    ax.set_xscale('log')

    yhigh = max(np.imag(
        didv._didvmean * time_phase
    )[plotinds][didv._freq[plotinds] < 1e5])
    ylow = min(np.imag(
        didv._didvmean * time_phase
    )[plotinds][didv._freq[plotinds] < 1e5])
    ybnd = np.max([yhigh, -ylow])

    ax.set_ylim([-ybnd, ybnd])
    ax.set_xlim([min(didv._freq[fitinds]), max(didv._freq[fitinds])])
    ax.legend(loc='upper left')
    ax.set_title("Imaginary Part of dIdV")
    ax.tick_params(which='both', direction='in', right=True, top=True)
    ax.grid(which='major')
    ax.grid(which='minor', linestyle='dotted', alpha=0.3)

    if lgcsave:
        fig.savefig(savepath + f"didv_imag_{savename}.png")
        plt.close(fig)
    else:
        plt.show()


def plot_abs_phase_didv(didv, poles="all", lgcsave=False, savepath="",
                        savename=""):
    """
    Function to plot the absolute value and the phase of the dIdV in
    frequency space. Currently creates two different plots.

    Parameters
    ----------
    didv : class
        The DIDV class object that the data is stored in
    poles : int, string, array_like, optional
        The pole fits that we want to plot. If set to "all", then plots
        all of the fits. Can also be set to just one of the fits. Can
        be set as an array of different fits, e.g. [1, 2]
    lgcsave : boolean, optional
        Boolean value on whether or not the figure should be saved
    savepath : string, optional
        Where the figure should be saved. Saved in the current
        directory by default.
    savename : string, optional
        A string to append to the end of the file name if saving. Empty
        string by default.

    """

    if poles == "all":
        poleslist = np.array([1,2,3])
    else:
        poleslist = np.array(poles)

    ## don't plot points with huge errors
    goodinds = np.abs(didv._didvmean / didv._didvstd) > 2.0
    fitinds = didv._freq > 0
    plotinds = np.logical_and(fitinds, goodinds)

    cost_lambda = lambda x: x['cost'] if x is not None else None
    dt_lambda = lambda x: x['params']['dt'] if x is not None else None

    cost_vals = [
        cost_lambda(didv._1poleresult),
        cost_lambda(didv._2poleresult),
        cost_lambda(didv._3poleresult),
    ]
    dt_vals = [
        dt_lambda(didv._1poleresult),
        dt_lambda(didv._2poleresult),
        dt_lambda(didv._3poleresult),
    ]
    if all(fv is None for fv in cost_vals):
        best_time_offset = 0
    else:
        min_cost_idx = min(
            (val, ii) for ii, val in enumerate(cost_vals) if val is not None
        )[1]
        best_time_offset = dt_vals[min_cost_idx]

    time_phase = np.exp(2.0j * np.pi * best_time_offset * didv._freq)

    ## plot the absolute value of the dIdV in frequency domain
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        didv._freq[plotinds],
        np.abs(didv._didvmean)[plotinds],
        color='blue',
        label='Mean',
        s=5,
    )
    ## plot error in absolute value of dIdV
    ax.plot(
        didv._freq[plotinds],
        np.abs((didv._didvmean + didv._didvstd))[plotinds],
        color='black',
        label='1-$\sigma$ Bounds',
        alpha=0.1,
    )
    ax.plot(
        didv._freq[plotinds],
        np.abs((didv._didvmean - didv._didvstd))[plotinds],
        color='black',
        alpha=0.1,
    )

    if (didv._1poleresult is not None) and (1 in poleslist):
        didvfit1_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(1)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.abs(didvfit1_freqdomain)[fitinds],
            color='magenta',
            label='1-Pole Fit',
        )

    if (didv._2poleresult is not None) and (2 in poleslist):
        didvfit2_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(2)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.abs(didvfit2_freqdomain)[fitinds],
            color='green',
            label='2-Pole Fit',
        )

    if (didv._3poleresult is not None) and (3 in poleslist):
        didvfit3_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(3)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.abs(didvfit3_freqdomain)[fitinds],
            color='orange',
            label='3-Pole Fit',
        )

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Abs($dI/dV$) ($\Omega^{-1}$)')
    ax.set_xscale('log')

    yhigh = max(np.abs(didv._didvmean)[plotinds][didv._freq[plotinds] < 1e5])

    ax.set_ylim(0, yhigh)
    ax.set_xlim(min(didv._freq[fitinds]), max(didv._freq[fitinds]))
    ax.legend(loc='upper left')
    ax.set_title("|dIdV|")
    ax.tick_params(which='both', direction='in', right=True, top=True)
    ax.grid(which='major')
    ax.grid(which='minor', linestyle='dotted', alpha=0.3)

    if lgcsave:
        fig.savefig(savepath + f"didv_abs_{savename}.png")
        plt.close(fig)
    else:
        plt.show()

    ## plot the phase of the dIdV in frequency domain
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        didv._freq[plotinds],
        np.angle(didv._didvmean * time_phase)[plotinds],
        color='blue',
        label='Mean',
        s=5,
    )

    ## plot error in phase of dIdV
    ax.plot(
        didv._freq[plotinds],
        np.angle((didv._didvmean + didv._didvstd) * time_phase)[plotinds],
        color='black',
        label='1-$\sigma$ Bounds',
        alpha=0.1,
    )
    ax.plot(
        didv._freq[plotinds],
        np.angle((didv._didvmean - didv._didvstd) * time_phase)[plotinds],
        color='black',
        alpha=0.1,
    )

    if (didv._1poleresult is not None) and (1 in poleslist):
        didvfit1_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(1)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.angle(didvfit1_freqdomain)[fitinds],
            color='magenta',
            label='1-Pole Fit',
        )

    if (didv._2poleresult is not None) and (2 in poleslist):
        didvfit2_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(2)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.angle(didvfit2_freqdomain)[fitinds],
            color='green',
            label='2-Pole Fit',
        )

    if (didv._3poleresult is not None) and (3 in poleslist):
        didvfit3_freqdomain = qp.complexadmittance(
            didv._freq, **didv.fitresult(3)['params'],
        )
        ax.plot(
            didv._freq[fitinds],
            np.angle(didvfit3_freqdomain)[fitinds],
            color='orange',
            label='3-Pole Fit',
        )

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Arg($dI/dV$)')
    ax.set_xscale('log')

    ax.set_ylim(-np.pi, np.pi)
    ax.set_xlim(min(didv._freq[fitinds]), max(didv._freq[fitinds]))

    ax.legend(loc='upper left')
    ax.set_title("Phase of dIdV")
    ax.tick_params(which='both', direction='in', right=True, top=True)
    ax.grid(which='major')
    ax.grid(which='minor', linestyle='dotted', alpha=0.3)

    if lgcsave:
        fig.savefig(savepath + f"didv_phase_{savename}.png")
        plt.close(fig)
    else:
        plt.show()
